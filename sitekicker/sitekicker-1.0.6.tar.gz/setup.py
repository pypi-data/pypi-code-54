# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sitekicker', 'sitekicker.entry', 'sitekicker.folder']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4',
 'jinja2',
 'markdown',
 'pygments',
 'pymdown-extensions',
 'pyyaml',
 'watchdog']

entry_points = \
{'console_scripts': ['sitekicker = sitekicker.__main__:main',
                     'sk = sitekicker.__main__:main']}

setup_kwargs = {
    'name': 'sitekicker',
    'version': '1.0.6',
    'description': 'Another static site generator',
    'long_description': "![build and deploy](https://github.com/nmhnmh/sitekicker/workflows/build%20and%20deploy/badge.svg?branch=master)\n\nThis is my **personal** static site generator, it lacks testings and documents at the moment.\nIf you need a static site generator, find one [here](https://www.staticgen.com/) with good community support.\n\n**SiteKicker** is yet another static site builder written in **Python3**(no support for python2).\n\nCurrent Project Status: **Beta, usable, but no testing and documentation**\n\n# Local development\n\nWe use [poetry](https://python-poetry.org/) to manage dependencies and virtual environments, make sure you have poetry installed, then in root directory of the project, run `poetry install` first to install all the dependencies and create the virtual environment, then run `poetry shell` to activate the virtual environment.\n\n# Dependencies: what and why\n\n* PyYAML: parse configurations(`site.yml` `folder.yml`) and entry front matters\n* Pygments: code highlighter\n* beautifulsoup4: working with html\n* markdown: markdown compiler\n* pymdown-extensions: markdown compiler extensions\n* Jinja2: a template engine\n* watchdog: local folder/file activity watcher\n\n## site.yml(or sitekicker.yml)\n\n```yml\n# Name of the site\nname: An Awesome Site\n# Base URL for the site, will be used to generate absolute urls\nbase_url: https://example.org\n# Directory where build output will be saved, could be relative path or absolute path\noutput_dir: .dist\n# Directory that contains layout/templates, default: templates, optional, supported template format is jinja2\ntemplate_dir: templates\n# Directories that will be copied, such as folders with assets or binary files\ncopy_dirs:\n  - assets\n```\n\n## folder.yml\n\n```yml\n# The options set in this file will be applied to all entries inside the folder where this file is found,\n# we refer to these entries as 'affected items of this file' below.\n# This is a good place to set some common options and flags.\n# You could also add any custom options below, prefix and tags are special because they has special meaning\n\n# The prefix will be prepended to all items affected by this file, 'article.html' will be 'abc/article.html'\n# if multiple prefix specified along the way, they will be concatenated and prefixed to the final url,\n# so if two prefix 'a' and 'b' specified, then the final url will be '/a/b/article.html'\nprefix: abc\n# The tags listed here will be added to all items affected by this file, tags specified at different places\n# will be merged, duplicate tags will be removed, original order of tags will be maintained\ntags:\n  - global tag 1\n  - global tag 2\n```\n\n## Entry Front Matter\n\n```yml\n# In this file your specified options for the entry, beside some predefined ones like 'id', 'title', 'date'\n# you can add your own custom options, and use it inside your templates, options specified here will override\n# options specified in meta.yml in parent folder, except 'prefix' and 'tags', the former will be concatenated,\n# the later will be merged\n\n# A unique id to identify the entry, no special chars, space will be substituted with hyphens, optional\n# when not set, will try to use file name as id, will emit an error when it is not possible\nid: some-thing-as-name\n# Title of the entry, mandatory, may contain any characters\ntitle: Sitekicker is another Static Site Generator\n# Date of the writing, mandatory, in the format of YYYY-MM-DD\ndate: 2016-10-20\n# Date of update, optional\nupdate_date: 2016-11-20\n# Tags that applies to this entry, optional\n# current entry will inherit all tags in its parent folders,\n# if folder 'a' contains tag 'a', folder 'a/b' contains tag 'b'\n# entry 'a/b/entry.md' contains tag 'c', then eventually the entry will\n# have there tags: 'a', 'b', 'c'\ntags:\n  - tag1\n  - tag2\n  - tag3\n```\n",
    'author': 'Minghao Ni',
    'author_email': 'niminghao804@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nmhnmh/sitekicker',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
