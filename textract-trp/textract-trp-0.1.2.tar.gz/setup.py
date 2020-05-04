# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['trp']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'textract-trp',
    'version': '0.1.2',
    'description': 'Parser for Amazon Textract results.',
    'long_description': '# Amazon Textract Results Parser - `textract-trp`\n\nAmazon *Textract Results Parser* or `trp` module packaged and improved for ease of use.\n\n## TL;DR\n\n```\npip install textract-trp\n```\n\nRequires Python 3.6 or newer.\n\n## Usage\n\n```python\nimport boto3\nimport trp\n\ntextract_client = boto3.client(\'textract\')\nresults = textract_client.analyze_document(... your file and other params ...)\ndoc = trp.Document(results)\n```\n\nNow you can examine `doc.pages`. For example print all the detected on the page:\n\n```python\nprint(doc.pages[0].text)\n```\n\nOr print out the detected tables in CSV format:\n\n```python\nfor row in doc.pages[0].tables[0].rows:\n    for cell in row.cells:\n        print(cell.text.strip(), end=",")\n    print()\n```\n\nOr retrieve text from a given position on the page. For that we have to create\n*Bounding Box* with the required coordinates relative to the page.\n\n```python\n# Coordinates are from top-left corner [0,0] to bottom-right [1,1]\nbbox = trp.BoundingBox(width=0.220, height=0.085, left=0.734, top=0.140)\nlines = doc.pages[0].getLinesInBoundingBox(bbox)\n\n# Print only the lines contained in the Bounding Box\nfor line in lines:\n    print(line.text)\n```\n\nRefer to the [Textract blog post](https://aws.amazon.com/blogs/machine-learning/automatically-extract-text-and-structured-data-from-documents-with-amazon-textract/)\nand to [amazon-textract-code-samples](https://github.com/aws-samples/amazon-textract-code-samples) GitHub repository for more details.\n\n## Background\n\nThe [Amazon blog post about Textract](https://aws.amazon.com/blogs/machine-learning/automatically-extract-text-and-structured-data-from-documents-with-amazon-textract/)\nrefers to a python module `trp.py` which used to be quite hard to find. There\nare many posts on the internet from people looking for the module, often confused by\nthe *"other trp module"* that\'s got nothing to do with Textract.\n\nHence I decided to package and publish the `trp.py` module from the\n[aws-samples/amazon-textract-code-samples](https://github.com/aws-samples/amazon-textract-code-samples)\nrepository. Fortunately its [MIT\nlicense](https://github.com/aws-samples/amazon-textract-code-samples/blob/master/LICENSE)\npermits that.\n\nOver time I have made some improvements to the module for ease of use.\n\n### Maintainer\n\n[Michael Ludvig](https://aws.nz)\n',
    'author': 'Michael Ludvig',
    'author_email': 'mludvig@logix.net.nz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mludvig/amazon-textract-trp',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
