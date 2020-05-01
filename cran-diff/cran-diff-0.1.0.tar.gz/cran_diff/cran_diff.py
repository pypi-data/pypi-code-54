from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Packages
from .models import Imports
from .models import Suggests
from .models import Exports


def make_querymaker(connect_string):
    """Instantiates QueryMaker class"""
    engine = create_engine(connect_string)
    Session = sessionmaker(bind=engine)
    query_maker = QueryMaker(Session())
    return query_maker


class NotFoundError(Exception):
    pass


class QueryMaker():
    def __init__(self, session):
        self.session = session


    def get_names(self):
        """Gets unique names of all packages in database

        return: list of package names
        """ 
        names = self.session.query(Packages.name).distinct()
        names = [element for tupl in names for element in tupl]
        return names

    
    def check_name_and_version(self, package_name, versions):
        """Checks that package name and version number are in database.
        Exception is raised if either are not.

        :params 
        package_name: string for the package name
        versions: list of version number strings
        """
        for version in versions:
            results = (self.session.query(Packages.version)
                                .filter(Packages.name == package_name, Packages.version == version))
            results = [element for tupl in results for element in tupl]
            if len(results) == 0:
                raise NotFoundError()


    def get_latest_versions(self, package_name):
        """Lists all versions of given package in database

        :param package_name: string for the package name
        :return: a list of the package version numbers
        """
        versions = (self.session.query(Packages.version)
                            .filter(Packages.name == package_name)
                            .order_by(Packages.date.desc()))
        versions = [element for tupl in versions for element in tupl]
        if len(versions) == 0:
            raise NotFoundError()
        return versions


    def query_imports(self, package_name, versions):
        """Get dictionary of package imports
            
        :params
        package_name: string for the package name
        versions: list of version number strings
        
        :return: a dictionary of imports with their version number
        """
        self.check_name_and_version(package_name, versions)
        import_list = []
        for version in versions:
            result = (self.session.query(Imports.name, Imports.version)
                            .join(Packages, Packages.id == Imports.package_id)
                            .filter(Packages.name == package_name, Packages.version == version))
            import_list.append(dict(result))
        return import_list

        
    def query_suggests(self, package_name, versions):
        """Get dictionary of package suggests
            
        :params
        package_name: string for the package name
        versions: list of version number strings
        
        :return: a dictionary of suggests with their version number
        """
        self.check_name_and_version(package_name, versions)
        suggest_list = []
        for version in versions:
            result = (self.session.query(Suggests.name, Suggests.version)
                            .join(Packages, Packages.id == Suggests.package_id)
                            .filter(Packages.name == package_name, Packages.version == version))
            suggest_list.append(dict(result))
        return suggest_list


    def query_exports(self, package_name, versions):
        """Get list of package exports
            
        :params
        package_name: string for the package name
        versions: list of version number strings
        
        :return: a list of exports
        """
        self.check_name_and_version(package_name, versions)
        export_list = []
        for version in versions:
            result = (self.session.query(Exports.name)
                            .join(Packages, Packages.id == Exports.package_id)
                            .filter(Packages.name == package_name, Packages.version == version))
            result = [i[0] for i in result]
            export_list.append(result)
        return export_list
        

def get_diff(result_list):
    """Get dictionary of diffs for imports and suggests
        
    :params
    result_list: output from query_imports() or query_suggests()
    :return: a dictionary with added, removed and changed (version numbers) packages
    """
    set1 = set(result_list[0].items())
    set2 = set(result_list[1].items())
    diff1 = set1 - set2
    diff2 = set2 - set1
    # Check for version changes
    changed = []
    added = []
    removed = []
    for i in diff1:
        was_changed = False
        for j in diff2:
            if i[0] == j[0]:
                changed.append((i[0], i[1], j[1]))
                was_changed = True
                break
        if not was_changed:
            added.append(i)
    for i in diff2:
        was_changed = False
        for j in diff1:
            if i[0] == j[0]:
                was_changed = True
                break
        if not was_changed:
            removed.append(i)
    added = [list(elem) for elem in added]
    removed = [list(elem) for elem in removed]
    changed = [list(elem) for elem in changed]
    return {'added': added,
            'removed': removed,
            'changed': changed}


def get_export_diff(result_list):
    """Get dictionary of diffs for exports
        
    :params
    result_list: output from query_exports()
    :return: a dictionary with added and removed packages
    """
    set1 = set(result_list[0])
    set2 = set(result_list[1])
    diff1 = set1 - set2
    diff2 = set2 - set1
    # Check for version changes
    changed = []
    added = []
    removed = []
    for i in diff1:
        added.append(i)
    for i in diff2:
        removed.append(i)
    return {'added': added,
            'removed': removed}
