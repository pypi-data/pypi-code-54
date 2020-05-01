# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sageup']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.12.49,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'colorama>=0.4.3,<0.5.0',
 'inquirer>=2.6.3,<3.0.0',
 'pprint>=0.1,<0.2',
 'pyfiglet>=0.8.post1,<0.9',
 'yaspin>=0.16.0,<0.17.0']

entry_points = \
{'console_scripts': ['sageup = sageup:main']}

setup_kwargs = {
    'name': 'sageup',
    'version': '0.1.2',
    'description': 'Interactive CLI tool for creating a SageMaker notebook instance from terminal, getting signed URL and opening it in browser',
    'long_description': '# SageUp\nInteractive CLI tool for creating a SageMaker notebook instance from terminal, getting signed URL and opening it in browser.\n\n![Screenshot](https://raw.githubusercontent.com/imankamyabi/sageup/master/images/sageup-demo.gif)\n\n\n## Installation:\n```shell\npip install sageup\n```\n\n## Usage\n\n### Run\nStarts an interactive session to create a SageMaker notebook instance and launch it in browser\n\n```shell\nsageup run\n```\n\n## Notes:\nDefault IAM role has full access to SageMaker and S3. Use a custom IAM role if need granular access, more security and protection against accidental change of resources by the notebook.\n\nMore features coming soon!\n\nAuthor: Iman Kamyabi\n \nFeedback: contact@imankamyabi.com',
    'author': 'Iman Kamyabi',
    'author_email': 'engkamyabi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/imankamyabi/sageup',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
