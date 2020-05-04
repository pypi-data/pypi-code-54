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
    'version': '0.1.2',
    'description': 'Animated plotting extension for Pandas with Matplotlib',
    'long_description': "# Pandas-Alive\n\nAnimated plotting extension for Pandas with Matplotlib\n\n**Pandas-Alive** is intended to provide a plotting backend for animated [matplotlib](https://matplotlib.org/) charts for [Pandas](https://pandas.pydata.org/) DataFrames, similar to the already [existing Visualization feature of Pandas](https://pandas.pydata.org/pandas-docs/stable/visualization.html).\n\nWith **Pandas-Alive**, creating stunning, animated visualisations is as easy as calling:\n\n``` python\ndf.plot_animated()\n```\n\n![Example Bar Chart](examples/example-barh-chart.gif)\n\n## Installation\n\nInstall with `pip install pandas-alive`\n\n## Usage\n\nAs this package builds upon [`bar_chart_race`](https://github.com/dexplo/bar_chart_race), the example data set is sourced from there.\n\nMust begin with a pandas DataFrame containing 'wide' data where:\n\n- Every row represents a single period of time\n- Each column holds the value for a particular category\n- The index contains the time component (optional)\n\nThe data below is an example of properly formatted data. It shows total deaths from COVID-19 for the highest 20 countries by date.\n\n![Example Data Table](https://raw.githubusercontent.com/dexplo/bar_chart_race/master/images/wide_data.png)\n[Example Table](examples/example_dataset_table.md)\n\nTo produce the above visualisation:\n\n- Set `output_file` for the visualisations to write to, or use `output_html` to return a HTML5 video\n- Call `plot_animated()` on the DataFrame\n- Done!\n\n``` python\nimport pandas_alive\n\ndf = pandas_alive.load_dataset()\n\npandas_alive.output_file('example-barh-chart.gif')\n\ndf.plot_animated()\n\n```\n\n### Currently Supported Chart Types\n\n`pandas-alive` current supports:\n\n- [Horizontal Bar Charts](#horizontal-bar-charts)\n- [Vertical Bar Charts](#vertical-bar-charts)\n- [Line Charts](#line-charts)\n\n#### Horizontal Bar Charts\n\n``` python\nimport pandas_alive\n\ndf = pandas_alive.load_dataset()\n\npandas_alive.output_file('example-barh-chart.gif')\n\ndf.plot_animated()\n```\n\n![Example Barh Chart](examples/example-barh-chart.gif)\n\n#### Vertical Bar Charts\n\n``` python\nimport pandas_alive\n\ndf = pandas_alive.load_dataset()\n\npandas_alive.output_file('example-barv-chart.gif')\n\ndf.plot_animated(orientation='v')\n```\n\n![Example Barv Chart](examples/example-barv-chart.gif)\n\n#### Line Charts\n\nWith as many lines as data columns in DataFrame.\n\n``` python\nimport pandas_alive\n\ndf = pandas_alive.load_dataset()\n\npandas_alive.output_file('example-line-chart.gif')\n\ndf.diff().plot_animated(kind='line')\n```\n\n![Example Line Chart](examples/example-line-chart.gif)\n\n### Multiple Charts\n\n`pandas-alive` supports multiple animated charts in a single visualisation.\n\n- Create each chart type ensure to disable writing to file with `write_to_file=False`\n- Create a list of all charts to include in animation\n- Use `animate_multiple_plots` with a `filename` and the list of charts (this will use `matplotlib.subplots`)\n- Done!\n\n``` python\nimport pandas_alive\n\ndf = pandas_alive.load_dataset()\n\nanimated_line_chart = df.diff().plot_animated(kind='line',write_to_file=False,period_length=200)\n\nanimated_bar_chart = df.plot_animated(kind='barh',write_to_file=False,period_length=200)\n\npandas_alive.animate_multiple_plots('example-bar-and-line-chart.gif',[animated_bar_chart,animated_line_chart]\n```\n\n![Example Bar & Line Chart](examples/example-bar-and-line-chart.gif)\n\n## Inspiration\n\nThe inspiration for this project comes from:\n\n- [bar_chart_race](https://github.com/dexplo/bar_chart_race) by [Ted Petrou](https://github.com/tdpetrou)\n- [Pandas-Bokeh](https://github.com/PatrikHlobil/Pandas-Bokeh) by [Patrik Hlobil](https://github.com/PatrikHlobil)\n\n## Contributing\n\nPull requests are welcome! Please help cover more and more chart types!\n\n## Requirements\n\nThis package utilises the [matplotlib.animation function](https://matplotlib.org/3.2.1/api/animation_api.html), thus requiring a writer library.\n\nEnsure to have one of the supported tooling software installed prior to use!\n\n- [ffmpeg](https://ffmpeg.org/)\n- [ImageMagick](https://imagemagick.org/index.php)\n- [Pillow](https://pillow.readthedocs.io/en/stable/)\n- See more at <https://matplotlib.org/3.2.1/api/animation_api.html#writer-classes>\n",
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
