from datetime import datetime, timedelta
import os
import shutil
import sys
import tarfile
import urllib.request

from bs4 import BeautifulSoup, SoupStrainer
from dateutil import parser
from deb_pkg_tools.control import deb822_from_string
from deb_pkg_tools.control import parse_control_fields
from deb_pkg_tools.deps import parse_depends
import requests
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

import cran_diff
from .cran_diff import NotFoundError
from .models import Packages
from .models import Imports
from .models import Suggests
from .models import Exports


def read_description_file(package):
    """Parses DESCRIPTION file

    :param: package: string for the package name
    :return: tuple of parsed description file metadata:
    title, description, url, bugreport, version, maintainer,
    date, import_dict, suggest_dict
    """
    description_file = f"{package}/DESCRIPTION"
    with open(description_file, "r", encoding ='utf-8') as desc_file:
        data = desc_file.read()
    unparsed_fields = deb822_from_string(data)
    parsed_fields = parse_control_fields(unparsed_fields)
    version = parsed_fields['Version']
    try:
        title = parsed_fields['Title']
    except KeyError:
        title = ''
    try:
        description = parsed_fields['Description']
    except KeyError:
        description = ''
    try:
        url = parsed_fields['Url']
    except KeyError:
        url = ''
    try:
        bugreport = parsed_fields['Bugreports']
    except KeyError:
        bugreport = ''
    try:
        maintainer = parsed_fields['Maintainer']
    except KeyError:
        maintainer = ''
    try:
        date = parsed_fields['Date/publication']
        # Parse datetimes
        try:
            date = parser.parse(date)
        except ValueError:
            date = parser.parse(date, dayfirst=True)
    except KeyError:
        try:
            date = parsed_fields['Date']
            # Parse datetimes
            try:
                date = parser.parse(date)
            except ValueError:
                date = parser.parse(date, dayfirst=True)
        except KeyError:
            date = None
    # Parse imports
    try:
        imports = parsed_fields['Imports']
        #Imports does not get parsed properly,
        #so do this here
        imports = parse_depends(imports)
        import_dict = create_relationship_dict(imports)
    except KeyError:
       import_dict = {}
    # Parse suggests
    try:
        suggests = parsed_fields['Suggests']
        suggest_dict = create_relationship_dict(suggests)
    except KeyError:
        suggest_dict = {}
    return (title, description, url,
            bugreport, version, maintainer, date,
            import_dict, suggest_dict)


def create_relationship_dict(field):
    """Creates a relationship dict for imports and suggests

    :param: field: string for the field name 
    :return: relationship dict with name of package as key 
    and version number as value
    """
    relationship = field.relationships
    #Create dict of name, version pairs
    package_dict = {}
    for i in relationship:
        version = ''
        if hasattr(i, 'version'):
            version = i.version
        package_dict[i.name] = version
    return package_dict


def read_namespace_file(package):
    """Parses NAMESPACE file for exports

    :param: package: string for the package name
    :return: list of exports
    """
    inner_list = []
    namespace_file = f"{package}/NAMESPACE"
    try:
        with open(namespace_file, "r", encoding ='ISO-8859-1') as nmspc_file:
            for i in nmspc_file:
                if i.startswith("export("):
                    func = i[len("export("):]
                    func = func.rstrip(")\n")
                    inner_list.append(func)
    except FileNotFoundError:
        return inner_list
    return inner_list


def database_insert(connect_string, package, version, date, title, description, url, bugreport, maintainer, imports, suggests, exports):
    """Creates SQLAlchemy engine and starts database session. Adds package information to database.

    :params: 
    connect_string: connection string for database
    package: string for the package name
    version: string for the version number
    date: datetime object for package publication date
    title: string for package title
    description: string for package description
    url: string for package URL
    bugreport: string for package bugreport
    maintainer: string for package maintainer
    imports: dict of import, version number pairs
    suggests: dict of suggests, version number pairs
    exports: list of exports
    """
    # create a configured "Session" class
    engine = create_engine(connect_string)
    Session = sessionmaker(bind=engine)

    # create a Session
    session = Session()

    package_info = Packages(name=package, version=version, date=date, title=title, description=description, maintainer=maintainer, url=url, bugreport=bugreport)
    session.add(package_info)
    session.commit()

    id_num = (session.query(Packages.id)
                     .filter(Packages.name == package, Packages.version == version)
                     .first()[0])
    for k, v in imports.items():
        import_info = Imports(package_id=id_num, name=k, version=v)
        session.add(import_info)
    session.commit()

    id_num = (session.query(Packages.id)
                     .filter(Packages.name == package, Packages.version == version)
                     .first()[0])
    for k, v in suggests.items():
        suggest_info = Suggests(package_id=id_num, name=k, version=v)
        session.add(suggest_info)
    session.commit()

    id_num = (session.query(Packages.id)
                     .filter(Packages.name == package, Packages.version == version)
                     .first()[0])
    for i in exports:
        export_info = Exports(package_id=id_num, name=i)
        session.add(export_info)
    session.commit()


def download_and_insert(connection_string, package, version):
    """Checks if package with version number is already in database. If not,
    it downloads package tar file from CRAN, unpacks the tar file, extracts 
    necessary information from the DESCRIPTION and NAMESPACE file and inserts 
    the information into the database. It then deletes the tar file and package directory.

    :params: 
    connection_string: connection string for database
    package: string for the package name
    version: string for the version number
    """
    query_maker = cran_diff.make_querymaker(connection_string)

    #Check if package (with version number) is already in database
    versions = []
    try:
        versions = query_maker.get_latest_versions(package)
    except NotFoundError:
        pass
    
    if len(versions) == 0 or version not in versions:
        # Download tar file
        path = 'https://cran.r-project.org/src/contrib/'
        tar_file = f'{package}_{version}.tar.gz'
        try:
            urllib.request.urlretrieve(f'{path}{tar_file}', tar_file)
        except urllib.error.HTTPError:
            try:
                path = f'https://cran.r-project.org/src/contrib/Archive/{package}/'
                urllib.request.urlretrieve(path + tar_file, tar_file)
            except urllib.error.HTTPError:
                raise ValueError(f'Could not download package archive for {package} v{version}')
        tar = tarfile.open(tar_file, "r:gz")
        tar.extractall()
        tar.close()
        #Extract necessary package info
        title, description, url, bugreport, version, maintainer, date, imports, suggests = read_description_file(package)
        exports = read_namespace_file(package)
        database_insert(connection_string, package, version, date, title, description, url, bugreport, maintainer, imports, suggests, exports)
        #Delete package and tarfile
        shutil.rmtree(package)
        os.remove(tar_file)


def get_archive_name_versions(package):
    """Scrapes package archive page to get previous version numbers
    within the last two years

    :param: package: string for the package name
    :return: list of archived versions within past two years
    """
    html_page = requests.get(f'https://cran.r-project.org/src/contrib/Archive/{package}/')
    soup = BeautifulSoup(html_page.text, 'html.parser')
    dates = [x.string.strip() for x in soup.select('body > table > tr > td:nth-child(3)') if len(x.string.strip()) > 0]
    version_list = []
    i = 0
    for link in BeautifulSoup(html_page.text, parse_only=SoupStrainer('a'), features="html.parser"):
        if link.has_attr('href'):
            if link['href'].startswith(package) and link['href'].endswith('.tar.gz'):
                date = dates[i]
                i += 1
                #Check if package older than 2 years
                date = parser.parse(date)
                two_years_ago = datetime.now() - timedelta(weeks=104)
                if two_years_ago > date:
                    continue
                version = link['href'].split('_')[1]
                version = version.rstrip('.tar.gz')
                version_list.append(version)
    return version_list


def download_and_insert_all_packages(connection_string, cran_metadata): 
    """Downloads and inserts package data into database, if not already there.
    Prints to stderr if exception is thrown.

    :params: 
    connection_string: connection string for database
    cran_metadata: package metadata from 'https://cran.rstudio.com/src/contrib/PACKAGES'
    """
    #Split into separate chunk for each package
    chunks = cran_metadata.split("\n\n")
    for chunk in chunks:
        try:
            unparsed_fields = deb822_from_string(chunk)
            parsed_fields = parse_control_fields(unparsed_fields)
            package = parsed_fields['Package']
            version = parsed_fields['Version']
            #If no version of package exists in database
            #Or if older version of package exists in database
            download_and_insert(connection_string, package, version)
            #Check archive to get previous version numbers
            #of all packages within last 2 years
            previous_versions = get_archive_name_versions(package)
            for version in previous_versions:
                download_and_insert(connection_string, package, version)
        except Exception as ex:
            print("#########################################################", file=sys.stderr)
            print(f'Exception: {type(ex)}', file=sys.stderr)
            print(ex, file=sys.stderr)
            print('---', file=sys.stderr)
            print('Package:', file=sys.stderr)
            print('---', file=sys.stderr)
            print(chunk, file=sys.stderr)
            print('---', file=sys.stderr)
            print("#########################################################", file=sys.stderr)


def populate_db(connection_string, test=True):
    """Populates the database with package info from CRAN

    :params: 
    connection_string: connection string for database
    
    Note: Running the lines below will download ALL 
    packages (including archives within last 2 years) and insert 
    these into database
    """
    
    #Test example
    if test:
        with open("../data/yesterday.txt", "r") as f:
            output = f.read()
            download_and_insert_all_packages(connection_string, output)
        with open("../data/today.txt", "r") as f:
            output = f.read()
            download_and_insert_all_packages(connection_string, output)
    else: 
        r = requests.get('https://cran.rstudio.com/src/contrib/PACKAGES')
        output = r.text
        download_and_insert_all_packages(connection_string, output)
