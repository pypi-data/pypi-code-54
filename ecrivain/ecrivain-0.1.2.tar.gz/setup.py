# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ecrivain']

package_data = \
{'': ['*']}

install_requires = \
['XlsxWriter>=1.2.8,<2.0.0']

setup_kwargs = {
    'name': 'ecrivain',
    'version': '0.1.2',
    'description': '',
    'long_description': "# README\n\nWrite nice formatted report with good enough formating.\n\n## Install\n\n## Usage\n\nWrite your dataframe with sensible default. No question asked.\n\n```python\nfrom ecrivain import xlsx\n\nxlsx.write_excel(df,'mytable.xlsx')\n```\n\nIf you want to have more control use `autofit`\n\n```python\nwriter = autofit(data,path,sheetname='data',factor=1.1,threshold=250)\nwriter.save()\n```\n\n",
    'author': 'Khalid',
    'author_email': 'khalidck@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
