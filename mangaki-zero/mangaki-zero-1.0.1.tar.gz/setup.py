# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zero', 'zero.tests']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.18,<2.0', 'pandas>=0.25.2,<0.26.0', 'scipy>=1.4.1,<2.0.0']

extras_require = \
{'deep': ['tensorflow'],
 'external': ['scikit-learn', 'surprise'],
 'fm': ['fastFM', 'pywFM']}

setup_kwargs = {
    'name': 'mangaki-zero',
    'version': '1.0.1',
    'description': "Mangaki's recommandation algorithms",
    'long_description': "# Zero\n\n[![Mangaki Zero's CI status](https://github.com/mangaki/zero/workflows/CI/badge.svg)](https://mangaki/zero/actions)\n[![Mangaki Zero's code coverage](https://codecov.io/gh/mangaki/zero/branch/master/graph/badge.svg)](https://codecov.io/gh/mangaki/zero)\n\n\n\nMangaki's recommendation algorithms.\n\nIt is tested on Python 3.6, 3.7 and 3.8 over OpenBLAS LP64 & MKL.\n\n## Usage\n\nMost models have the following routines:\n\n    from zero.als import MangakiALS\n    model = MangakiALS(nb_components=10)\n    model.fit(X, y)\n    model.predict(X)\n\nThere are a couple of other methods that can be used for online fit, say `model.predict_single_user(work_ids, user_parameters)`.\n\nTo run k-fold cross-validation, do:\n\n    python compare.py <path/to/dataset>\n\n## Results\n\n### Mangaki data\n\n![Comparing on Mangaki](results/mangaki.png)\n\n### Movielens data\n\n![Comparing on Movielens](results/movielens.png)\n\nFeel free to use. Under GPLv3 license.\n",
    'author': 'Jill-Jênn Vie',
    'author_email': 'vie@jill-jenn.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://research.mangaki.fr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
