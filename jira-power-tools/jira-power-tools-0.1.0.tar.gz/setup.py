# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['jirapt']

package_data = \
{'': ['*']}

install_requires = \
['jira>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'jira-power-tools',
    'version': '0.1.0',
    'description': 'Tools to improve working with the python jira API.',
    'long_description': '# jira power tools\n\nA collection of tools to make it easier to work with the \n[Python Jira API](https://pypi.org/project/jira/).\n\n## Usages\n\n### Lazy Pagination of Jira Issues\n\nIf you are querying a lot of jira issues. Paginating the results can lighten the memory usage\non the Jira server. But needing to keep track of the pagination is painful. Using lazy pagination\ngives you an iterable that can track pagination for you:\n\n```python\nimport jirapt\n\njira = # jira server instance.\njql = "JQL query"\n\nissues = jirapt.search_issues(jira, jql, ...) # you can include any parameters you might pass to search_issues.\n\nfor issue in issues:\n    # perform work on issue\n\n```\n',
    'author': 'David Bradford',
    'author_email': 'david.bradford@mongodb.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/...',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
