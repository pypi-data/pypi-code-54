# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['django_wools']

package_data = \
{'': ['*']}

install_requires = \
['django>1.7.0', 'psutil>2.0.0', 'tqdm>3.0.0', 'zopflipy>1.1']

setup_kwargs = {
    'name': 'django-wools',
    'version': '0.1.1',
    'description': 'Django tools from WITH',
    'long_description': 'Django Wools\n============\n\nDjango tools from WITH.\n\nThat\'s a collection of things that we at [WITH](https://with-madrid.com/) got\ntired of copy/pasting in every project.\n\n## Install\n\n```\npip install django_wools\n```\n\n## Included Wools\n\n### Storage\n\n#### `django_wools.storage.GzipManifestStaticFilesStorage`\n\nThat\'s a sub-class of the \n[ManifestStaticFilesStorage](https://docs.djangoproject.com/en/3.0/ref/contrib/staticfiles/#manifeststaticfilesstorage)\nbut that makes sure that along with all the files comes a `.gz` version which\nis easy to pick up for nginx (or other static files server).\n\n### Middlewares\n\n#### `django_wools.middlewares.NowMiddleware`\n\nSuppose that you have a content that is available up until a given date. When\nthe date is passed then everything related to this content expires. However,\nin order to do this, you\'re probably going to make several request, possibly in\nloosely connected parts of your code. In those cases, when looking at the time,\nthe clock will show different value as the time passes between calls. It means\nthat you could very well end up with one half of your code considering that the\nobject is still valid but the other half that it expired.\n\nIn order to prevent this, the simplest is to consider that the time is fixed\nand that the code executes instantly at the moment of the request. The goal\nof this middleware is to save the current time at each request and then to\nprovide an easy way to get the current time through the request.\n\nIf the middleware is activated, you should be able to get the time like this:\n\n```python\nfrom time import sleep\nfrom django.shortcuts import render\n\ndef my_view(request):\n    print(f"Now is {request.now()}")\n    sleep(42)\n    print(f"Now is still {request.now()}")\n\n    return render(request, "something.html", {"now": request.now()})\n```\n\n### Database\n\n#### `django_wools.db.require_lock`\n\nProvides a way to explicitly generate a PostgreSQL lock on a table.\n\nBy example:\n\n```python\nfrom django.db.transaction import atomic\nfrom django_wools.db import require_lock\n\nfrom my_app.models import MyModel\n\n\n@atomic\n@require_lock(MyModel, \'ACCESS EXCLUSIVE\')\ndef myview(request):\n    # do stuff here\n```\n',
    'author': 'Rémy Sanchez',
    'author_email': 'remy.sanchez@with-madrid.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/WithIO/django-wools',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
