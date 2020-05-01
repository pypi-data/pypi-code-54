# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bookops_worldcat']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23,<3.0']

setup_kwargs = {
    'name': 'bookops-worldcat',
    'version': '0.2.0',
    'description': 'OCLC WorldCat Search and Metadata APIs wrapper',
    'long_description': '[![Build Status](https://travis-ci.com/BookOps-CAT/bookops-worldcat.svg?branch=master)](https://travis-ci.com/BookOps-CAT/bookops-worldcat) [![Coverage Status](https://coveralls.io/repos/github/BookOps-CAT/bookops-worldcat/badge.svg?branch=master&service=github)](https://coveralls.io/github/BookOps-CAT/bookops-worldcat?branch=master) [![PyPI version](https://badge.fury.io/py/bookops-worldcat.svg)](https://badge.fury.io/py/bookops-worldcat) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/bookops-worldcat) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)    \n\n# bookops-worldcat  \n**Early ALPHA version**\n\nA WorldCat Search and Metadata APIs wrapper abstracting OCLC\'s boilerplate.  \nBookOps-Worldcat simplifies requests to these web services making them more accessible to OCLC member libraries.\n\n## Installation\n\nUse pip:\n\n`$ pip install bookops-worldcat`\n\n## Documentation\n\nFor full documentation please see https://bookops-cat.github.io/bookops-worldcat/\n\n## Features\n\nThis package takes advantage of functionality of a popular [Requests library](https://requests.readthedocs.io/en/master/). Interactions with [OCLC](https://www.oclc.org/en/home.html)\'s services are built around Requests\' sessions. Authorizing a session simply requires passing OCLC\'s WSkey (`SearchSession`) or an access token (`MetadataSession`). Opening a session allows the user to call specific methods to facilitate communication between the user\'s script/client and a particular endpoint of OCLC\'s service. Many of the hurdles related to making valid requests are hidden under the hood of this package, making it as simple as possible.  \nPlease note, not all functionalities of Worldcat Search and Metadata APIs are implemented as this tool was built primarily for the BookOps organization\'s specific needs. We are open to any collaboration to expand and improve this package.  \n\nAt the moment, BookOps-Worldcat supports requests to following OCLC\'s web services:  \n\n+ [Authentication via Client Credential Grant](https://www.oclc.org/developer/develop/authentication/oauth/client-credentials-grant.en.html)\n+ [WorldCat Search API](https://www.oclc.org/developer/develop/web-services/worldcat-search-api.en.html\n)  \n    + SRU\n    + Read\n    + Lookup By ISBN\n    + Lookup By ISSN\n    + Lookup By Standard Number\n+ [Worldcat Metadata API](https://www.oclc.org/developer/develop/web-services/worldcat-metadata-api.en.html)\n    + Read\n    + Set/Create\n    + Unset/Delete\n    + Retrieve Status\n    + Batch Set\n    + Batch Unset\n\n\nBasic usage:\n```python\n>>> from bookops_worldcat import SearchSession\n>>> session = SearchSession(credentials="your_WSkey")\n>>> result = session.lookup_oclc_number("1143317889")\n>>> print(result)\n<Response [200]>\n```\n\nContext manager:\n```python\nwith SearchSession(credentials="your_WSkey") as session:\n    results = session.lookup_isbn("9781680502404")\n    print(results.text)\n```\n```xml\n<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<record xmlns="http://www.loc.gov/MARC21/slim">\n    <leader>00000cam a2200000 i 4500</leader>\n    <controlfield tag="001">1143317889</controlfield>\n    <controlfield tag="008">200305t20202019nyuabf   b    001 0 eng c</controlfield>\n    <datafield ind1=" " ind2=" " tag="010">\n      <subfield code="a">  2018957420</subfield>\n    </datafield>\n    <datafield ind1=" " ind2=" " tag="020">\n      <subfield code="a">9780316230049</subfield>\n      <subfield code="q">(pbk.)</subfield>\n    </datafield>\n    <datafield ind1=" " ind2=" " tag="020">\n      <subfield code="a">0316230049</subfield>\n    </datafield>\n    <datafield ind1="1" ind2=" " tag="100">\n      <subfield code="a">Christakis, Nicholas A.,</subfield>\n      <subfield code="e">author.</subfield>\n    </datafield>\n    <datafield ind1="1" ind2="0" tag="245">\n      <subfield code="a">Blueprint :</subfield>\n      <subfield code="b">the evolutionary origins of a good society /</subfield>\n      <subfield code="c">Nicholas A. Christakis.</subfield>\n    </datafield>\n      ...\n</record>\n```\n\n## Changelog\n\nConsult the [Changelog page](https://bookops-cat.github.io/bookops-worldcat/changelog/) for fixes and enhancements of each version. \n\n## Bugs/Requests  \n\nPlease use [Github issue tracker](https://github.com/BookOps-CAT/bookops-worldcat/issues) to submit bugs or request features.\n',
    'author': 'Tomasz Kalata',
    'author_email': 'klingaroo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://bookops-cat.github.io/bookops-worldcat/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
