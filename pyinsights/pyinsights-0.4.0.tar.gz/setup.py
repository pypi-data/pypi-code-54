# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyinsights', 'pyinsights.cli']

package_data = \
{'': ['*'], 'pyinsights': ['schema/*']}

install_requires = \
['boto3>=1.10.45,<2.0.0', 'jsonschema>=3.2.0,<4.0.0', 'pyyaml>=5.2,<6.0']

entry_points = \
{'console_scripts': ['pyinsights = pyinsights.cli:run']}

setup_kwargs = {
    'name': 'pyinsights',
    'version': '0.4.0',
    'description': 'AWS CloudWatch Logs Insights is wrapped by Python',
    'long_description': "# PyInsights\n\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyinsights)\n![PyPI](https://img.shields.io/pypi/v/pyinsights?color=blue)\n![GitHub](https://img.shields.io/github/license/homoluctus/pyinsights)\n\nA CLI tool To query CloudWatch Logs Insights.\n\n![usage1](https://raw.githubusercontent.com/homoluctus/pyinsights/master/images/usage1.png)\n\n![usage2](https://raw.githubusercontent.com/homoluctus/pyinsights/master/images/usage2.png)\n\n**ToC**\n\n<!-- TOC depthFrom:2 -->\n\n- [Usage](#usage)\n  - [Write Configuration](#write-configuration)\n  - [Execute command](#execute-command)\n- [Configuration](#configuration)\n  - [version](#version)\n  - [log_group_name](#log_group_name)\n  - [query_string](#query_string)\n  - [duration](#duration)\n    - [type: string](#type-string)\n    - [type: object](#type-object)\n  - [limit](#limit)\n- [CLI Options](#cli-options)\n- [Environment Variable](#environment-variable)\n\n<!-- /TOC -->\n\n## Usage\n\n### Write Configuration\n\nWrite configuration to `pyinsights.yml` like:\n\n```yaml\nversion: '1.0'\nlog_group_name:\n  - '/ecs/sample'\nquery_string: 'field @message | filter @message like /ERROR/'\nduration: '30m'\nlimit: 10\n```\n\nI wrote examples, so see [examples folder](https://github.com/homoluctus/pyinsights/tree/master/examples).\n\n### Execute command\n\n```bash\npyinsights -c pyinsights.yml -p aws_profile -r region\n```\n\n## Configuration\n\n### version\n\n|Type|Required|\n|:--:|:--:|\n|string|true|\n\nChoose configuration version from ['1.0']\n\n### log_group_name\n\n|Type|Required|\n|:--:|:--:|\n|array|true|\n\nTarget log group names to query\n\n### query_string\n\n|Type|Required|\n|:--:|:--:|\n|string or array|true|\n\nSpecify CloudWatch Logs Insights query commands.\nPlease see [CloudWatch Logs Insights Query Syntax](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax.html).\n\n:warning: If query_string type is array, Unix-style pipe `|` is not required. Execute in order from the top.\n\nex)\n\n```yml\nquery_string:\n  - 'field @message'\n  - 'fileter @message like /WARN/'\n```\n\nEqual to\n\n```yml\nquery_string: 'field @message | fileter @message like /WARN/'\n```\n\n### duration\n\n|Type|Required|\n|:--:|:--:|\n|string or object|true|\n\n#### type: string\n\nSpecify weeks, days, hours, minutes or seconds unit.\n\n```\nweeks = w\ndays = d\nhours = h\nminutes = m\nseconds = s\n```\n\nex)\n\n```yml\nduration: 10h\n```\n\n#### type: object\n\nSpecify `start_time` and `end_time`.\nThe format must be `YYYY-MM-DD HH:MM:SS`.\n\nex)\n\n```yml\nduration:\n  start_time: '2020-01-01 00:00:00'\n  end_time: '2020-01-01 01:00:00'\n```\n\n### limit\n\n|Type|Required|\n|:--:|:--:|\n|integer|false|\n\nThe number of log to fetch.\nOf course, you can specify `limit` in [query_string](#query_string).\n\n## CLI Options\n\n|Option|Required|Description|\n|:--:|:--:|:--|\n|-c, --config|true|Specify yaml configuration by absolute or relative path|\n|-f, --format|false|Choose from json or table|\n|-p, --profile|false|AWS profile name|\n|-r, --region|false|AWS region|\n|-q, --quiet|false|Suppress progress message|\n|-o, --output|false|Specify the filename to output the query result|\n|-v, --version|false|Show version|\n\n## Environment Variable\n\nIf `profile` and `region` options are not specified, AWS Credentials must be set as environment variables.\n\n- AWS_ACCESS_KEY_ID\n- AWS_SECRET_ACCESS_KEY\n- AWS_DEFAULT_REGION\n\nPlease see [Environment Variable Configuration](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html#environment-variable-configuration) for the detail.\n",
    'author': 'homoluctus',
    'author_email': 'w.slife18sy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/homoluctus/pyinsights',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
