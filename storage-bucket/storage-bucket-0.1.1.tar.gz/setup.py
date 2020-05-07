# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['storage_bucket']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.3.0,<20.0.0',
 'google-cloud-storage>=1.28.1,<2.0.0',
 'returns>=0.13.0,<0.14.0']

setup_kwargs = {
    'name': 'storage-bucket',
    'version': '0.1.1',
    'description': 'Easy to work with Google Cloud Platform Storage Bucket wrapper',
    'long_description': "# Google Cloud Platform Storage Bucket EaseyBreezey\n\nThis package just aims to make life a little bit easier for people who have to work with google cloud storage bucket.\n\n\n## Quickstart:\n\n1. get the package\n  * `pip install storage-bucket`\n2. Download your keyfile and save it as key.json and point to it with env var:\n  * `gcloud iam service-accounts keys create key.json --iam-account your_service_account@your_project.iam.gserviceaccount.com`\n  * `export GOOGLE_APPLICATION_CREDENTIALS='key.json'`\n3. Run some code:\n\n\n```python\nfrom storage_bucket.download_file import DownloadFile, download_file\n\n\ndef use_data_for_something(data):\n    print(data)\n\n# Returns Modal way\ndownloader = DownloadFile()\ndownloader(\n    'my_bucket',\n    'my_file.txt',\n).map(\n    use_data_for_something,  # send data to this function,\n).alt(\n    print,  # print error or send a mail or w/e\n)\n\n# Normal way, this might throw exception.\nmy_data = download_file(\n    'my_bucket',\n    'my_file.txt',\n)\nprint(my_data)\n```\n\n### The use of [Returns](https://github.com/dry-python/returns) library.\n  * Just lets us get rid of all exceptions.\n  * Lets us chain stuff so everything looks good.\n  * Lets you use `DownloadFile()(args...).bind(dostuff).alt(dostuffonfailure)`\n  * Don't like it? use the matching normal function provided for your convenience.\n\n\n",
    'author': 'Thomas Borgen',
    'author_email': 'thomas@borgenit.no',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
