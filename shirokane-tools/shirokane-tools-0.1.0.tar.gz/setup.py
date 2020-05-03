# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shirokane_tools']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['array_job_task_runner = shirokane_tools.qsub_tasks:array_job_task_runner',
                     'run_tasks = shirokane_tools.qsub_tasks:run_tasks']}

setup_kwargs = {
    'name': 'shirokane-tools',
    'version': '0.1.0',
    'description': 'My SHIROKANE tools',
    'long_description': None,
    'author': 'Hiroki Konishi',
    'author_email': 'relastle@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
