# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['phk_logger']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'phk-logger',
    'version': '0.1.2',
    'description': 'An uncomplicated way to use logger inside python applications',
    'long_description': '![ProHacktive](https://prohacktive.io/storage/parameters_images/LmQm4xddzmyFAdGYvQ32oZ9t1P9e8098UubYjnE9.svg "PHK-Logger from ProHacktive.io")\n\n# PHK-Logger\n\nAn uncomplicated way to use logger inside python applications\n\n---\n- Created at: 01/05/2020\n- Updated at:\n- Author: Ben Mz (bmz)\n- Maintainer: Ben Mz (bmz)\n- Client: ProHacktive (https://prohacktive.io)\n\n## Install\nThe easy way is by using pip\n```bash\npip install phk-logger\n```\n  \nThe harder way is from sources\n```bash\ngit clone https://github.com/proh4cktive/phk-logger.git\ncd phk-logger\npython install setup.py\n```\n\n## Usage\nPHK-Logger is a lib so you just have to import it when needed\n```python\n#!/usr/bin/env python\n# -*- coding: utf-8 -*-\n\nfrom phk_logger import PHKLogger as Logger\n```\n  \nThen in your code you can instantiate it directly\n```python\nlogger = Logger(name=\'mytest\', cli=True)\n```\n  \nAnd use it when needed\n```python\nlogger.info(\'This is an info message\') # Will not be printed as default level is Warning\nlogger.write(\'A blue warning\', level=\'warning\', color=\'blue\')\n```\n\n## Options\nPHK-Logger is configred by default to output log event to your SysLog sub-system (Only supports Linux/MacOS). Some additional options can be set in order to change this behaviour.  \n\n- **name** Set a specific name to your logger stream, by default will use the `__name__` var.\n- **level** Set the log level, must be a level from logging package\n- **filename** If set phk-logger will output events to a specific filename using *TimedRotatingFileHandler* configured with a file rotating every midnight, and 3 backup files\n- **backup** Only used if **filename** is configured, specifiy the number of backup to keep\n- **when** Only used if **filename** is configured, specify when to execute the file rotation\n- **cli** If set to True this will also output log event to command line interface (CLI). Only useful for debugging app.\n- **pattern** Define the log pattern to use for event output. Default is `%(name)s %(asctime)s %(levelname)-8s %(message)s`\n\n\n\n## Methods\nSeveral methods can be used to generate event logs, they all support the same options (only usefuls when using **cli** flag):  \n\n- msg: the message to output\n- color: override the default color\n- light: override the light mode\n\n> - **debug**(msg, color=\'blue\', light=True) output event with prefix: `[*]`\n> - **info**(msg, color=\'green\', light=False) output event with prefix: `[+]`\n> - **warning**(msg, color=\'yellow\', light=False) output event with prefix: `[-]`\n> - **error**(msg, color=\'red\', light=False) output event with prefix: `[!]`\n> - **critical**(msg, color=\'red\', light=True) output event with prefix: `[!]`\n  \nAn additional method is accessible which support a level parameter\n> - **write**(message, level=None, color=None, light=None)\n\n### Colors\nMultiple colors are supported (case insensitive)\n- BLACK\n- BLUE\n- GREEN\n- CYAN\n- RED\n- PURPLE\n- YELLOW\n- WHITE\n- no-color (default)\n\n### Levels\nMultiple levels are supported (case insensitive)\n- DEBUG\n- INFO\n- INFOS\n- WARNING\n- ERROR\n- CRITICAL\n  \n\n## TODO\n- Unit Tests\n- Doc',
    'author': 'Ben Mz',
    'author_email': 'bmz@prohacktive.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
