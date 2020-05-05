# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['leapfrog']

package_data = \
{'': ['*']}

install_requires = \
['Flask-Session>=0.3.1',
 'argon2-cffi>=19.2.0',
 'black',
 'dash-bootstrap-components>=0.8.1',
 'dash-extra-components>=0.0.1',
 'dash-table>=4.5.1',
 'dash>=1.7.0',
 'dill>=0.3.1.1',
 'docutils>=0.16',
 'fastparquet>=0.3.2',
 'flask_caching>=1.3.3',
 'flask_login>=0.4.1',
 'ipykernel>=5.1.0',
 'libsass>=0.19.4',
 'matplotlib>=3.1.2',
 'pandas>=0.25.3',
 'papermill>=1.2.1',
 'pexpect>=4.7.0',
 'plotly>=4.4.1',
 'psutil>=5.6.7',
 'pyarrow>=0.15.1',
 'python-box>=4.2.3',
 'redis>=3.3.11',
 'ruamel.yaml>=0.15.8',
 'scikit-image>=0.15.0',
 'scikit-learn>=0.22.1',
 'shap>=0.34.0',
 'sklearn-pandas>=1.8.0',
 'statsmodels>=00.10.2',
 'tables>=3.6.1',
 'tqdm>=4.41.1',
 'werkzeug<1.0',
 'xlsxwriter>=1.2.7']

extras_require = \
{':sys_platform == "linux"': ['python-snappy>=0.5.4', 'dlib>=19.19.0'],
 'circleci': ['pytest-circleci-parallelized']}

setup_kwargs = {
    'name': 'leapfrog',
    'version': '0.0.1',
    'description': 'Boost productivity by using a range of tools helping with ETL, modelling, reporting, and dashboards',
    'long_description': '# Leapfrog\n\nThis is placeholder until the package is released properly',
    'author': 'Jan Beitner',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': '',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
