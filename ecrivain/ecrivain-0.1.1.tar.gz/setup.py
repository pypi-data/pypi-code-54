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
    'version': '0.1.1',
    'description': '',
    'long_description': "README\n======\n\nWrite nice formatted report with good enough formating.\n\nInstall\n-------\n\nUsage\n-----\n\nWrite your dataframe with sensible default. No question asked.\n\n.. code:: python\n\n   from ecrivain import xlsx\n\n   xlsx.write(df,'mytable.xlsx')\n\nIf you want to have more control use ``autofit``\n\n.. code:: python\n\n   writer = autofit(data,path,sheetname='data',factor=1.1,threshold=250)\n   writer.save()\n",
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
