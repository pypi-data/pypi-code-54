# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['simulert', 'simulert.handlers', 'simulert.tests']

package_data = \
{'': ['*']}

install_requires = \
['poetry>=1.0,<2.0', 'slackclient>=2.5,<3.0']

setup_kwargs = {
    'name': 'simulert',
    'version': '0.1.0',
    'description': 'A package to provide useful functionality for sending alerts about running simulations.',
    'long_description': '# simulert\nA package for generating alerts about simulations.\n\n## Installation\nThis project has not made it to Pypi so installation will require cloning the repository\nand adding it as a development package with either `pip install -e /path/to/simulert` or\n`conda develop /path/to/simulert`.\n\n## Usage\nThis package is architected similarly to Python\'s built-in logging package.\nAn `Alerter` class is instantiated with `getAlerter` and this class is triggered to send\nalerts which are distributed to all the handlers registered with that class.\n\nCurrent handlers include a logger (default), an emailer and a slack client.\n\nThe `Alerter` currently provides two ways to trigger alerts: most simply,calling the\n`alert` method with a message; and possibly more conveniently, with the\n`simulation_alert` context wrapping the simulation code.\n\n## Example\n```python\nfrom simulert import getAlerter\nfrom simulert.handlers import Emailer, Slacker\n\nemailer = Emailer(\n    "username",\n    "password",\n    ("Simulations", "noreply_simulations@company.com"),\n    ("Data scientist", "scientist@company.com"),\n    "smtp.mailserver.company.com",\n)\nslacker = Slacker("slack_app_token", "username")\nalerter = getAlerter().add_handler(emailer).add_handler(slacker)\nwith alerter.simulation_alert("super dooper sim"):\n    run_simulation()\n```\n\n## TODO\n1. Complete docstrings\n1. Test email.py, logs.py and slack.py\n1. Add default handler args that read environment variables\n1. Write a better README.md\n1. Tidy up pyproject.toml to include only necessary files\n1. Setup Github\n    1. Automated testing\n    1. Branch protection\n1. Deploy to Pypi via github with version management\n1. Add a changelog\n1. Add a logging handler as an event source.',
    'author': 'Jeremy Minton',
    'author_email': 'jeremyminton@gmail.com',
    'url': 'https://github.com/jjminton/simulert',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
