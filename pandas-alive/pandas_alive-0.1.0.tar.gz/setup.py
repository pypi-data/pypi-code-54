# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pandas_alive']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.2.1,<4.0.0', 'pandas>=1.0.3,<2.0.0']

setup_kwargs = {
    'name': 'pandas-alive',
    'version': '0.1.0',
    'description': 'Animated plotting extension for Pandas with Matplotlib',
    'long_description': '# Pandas-Alive\n\nAnimated plotting extension for Pandas with Matplotlib\n\n**Pandas-Alive** is intended to provide a plotting backend for animated [matplotlib](https://matplotlib.org/) charts for [Pandas](https://pandas.pydata.org/) DataFrames, similar to the already [existing Visualization feature of Pandas](https://pandas.pydata.org/pandas-docs/stable/visualization.html).\n\nWith **Pandas-Alive**, creating stunning, animated visualisations is as easy as calling:\n\n``` python\ndf.plot_animated()\n```\n\n## Inspiration\n\nThe inspiration for this project comes from:\n\n- [bar_chart_race](https://github.com/dexplo/bar_chart_race) by [Ted Petrou](https://github.com/tdpetrou)\n- [Pandas-Bokeh](https://github.com/PatrikHlobil/Pandas-Bokeh) by [Patrik Hlobil](https://github.com/PatrikHlobil)\n\n`bar_chart_race` produces animations from DataFrames like:\n\n![bar_chart_race example](https://raw.githubusercontent.com/dexplo/bar_chart_race/master/videos/covid19_horiz_desc.gif)\n',
    'author': 'JackMcKew',
    'author_email': 'jackmckew2@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
