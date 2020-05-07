#!/usr/bin/env python
#   -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'pybuilder-archetype-api',
        version = '0.1.1',
        description = 'External plugin for PyBuilder to generate a web service project structure',
        long_description = "# PyBuilder Archetype API Plugin\n\nThis plugin generates a structure for a project that requieres endpoints (APIs or web services). This plugin needs\n[pybuilder_archetype_base](https://github.com/yeuk0/pybuilder-archetype-base) due to its dependancy with one of its\ntasks (`create_archetype_api`).\n\nIn the following diagram there is every directory and file created during `create_archetype_api` execution (take note\n that `create_archetype_base` task will add more packages and directories -check its `README.md` file for more\n information):\n\n```text\nsrc\n└── package_name\n    ├── api  # For every script related with the web services\n    |   ├── __init__.py\n    |   └── api_example.py\n    ├── config\n    |   ├── __init__.py\n    |   └── constants.py\n    ├── __init__.py\n    ├── gunicorn_config.py  # Gunicorn launching configuration\n    ├── main.py  # Script with Flask app\n    └── wsgi.py  # WSGI file for server launch\nrequirements.txt\n```\n\nContent from `requirements.txt` and `constants.py` files will be added to the currently existing ones, trying to keep\n the values set by other plugins.\n\n## How to use pybuilder_archetype_api\n\n> **NOTICE**: This plugin only works on Windows due to its dependency with pybuilder_archetype_base PyBuilder plugin.\nUsing this plugin in other OS shall not work properly. Multi-platform support soon.\n\nAdd plugin dependencies to your `build.py` (it requires [pybuilder_archetype_base](https://github.com/yeuk0/pybuilder-archetype-base) and [pybuilder_pycharm_workspace](https://github.com/yeuk0/pybuilder-pycharm-workspace)\nto work properly):\n\n```python\nuse_plugin('pypi:pybuilder_pycharm_workspace')\nuse_plugin('pypi:pybuilder_archetype_base')\nuse_plugin('pypi:pybuilder_archetype_api')\n```\n\nConfigure the plugin within your `init` function:\n\n```python\n@init\ndef initialise(project):\n    project.set_property('project_base_path', project_path)\n```\n\nThis will tell the plugin which is the project location in the filesystem. `project_base_path` property value should\n be always the same.\n\nLaunch the task with:\n\n```console\n(venv) C:\\Users\\foo\\PycharmProjects\\bar> pyb create_archetype_api\n```\n\n### `build.py` file recommended\n\nCheck [pybuilder_archetype_base `build.py` recommendation](https://github.com/yeuk0/pybuilder-archetype-base#buildpy-file-recommended).\n\n## Properties\n\nPlugin has next properties with provided defaults\n\n| Name | Type | Default Value | Description |\n| --- | --- | --- | --- |\n| project_base_path | Path | None | Project's path in filesystem (same as `build.py` file). Mandatory |\n",
        long_description_content_type = 'text/markdown',
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python'
        ],
        keywords = '',

        author = 'Arturo GL, Diego BM',
        author_email = 'r2d2006@hotmail.com, diegobm92@gmail.com',
        maintainer = '',
        maintainer_email = '',

        license = 'Apache License, Version 2.0',

        url = 'https://github.com/yeuk0/pybuilder-archetype-api',
        project_urls = {},

        scripts = [],
        packages = [
            'pybuilder_archetype_api',
            'pybuilder_archetype_api.resources'
        ],
        namespace_packages = [],
        py_modules = [],
        entry_points = {},
        data_files = [],
        package_data = {
            'pybuilder_archetype_api': ['resources/*', 'resources/api/*', 'resources/config/*']
        },
        install_requires = [],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        python_requires = '',
        obsoletes = [],
    )
