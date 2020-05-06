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
        name = 'pybuilder-archetype-base',
        version = '0.1.1',
        description = 'External plugin for PyBuilder to generate a base project structure',
        long_description = '# PyBuilder Archetype Base Plugin\n\nThis plugin generates a base common structure with no major dependecies. The main idea is to get an skeleton that can\n be used for any kind of Python module. It modifies PyBuilder structure logic lightly, removing some packages making\n  it less _Java-like_.\n\nIn the following diagram there is every directory and file created during `create_archetype_base`:\n\n```text\nbin\ndocs\nsrc\n└── package_name\n    ├── config  # For any kind of configuration files or constants\n    |   ├── logger\n    |   |   └── logger.yml\n    |   ├── __init__.py\n    |   ├── constants.py\n    |   └── messages.py\n    ├── core  # Logic of the project itself\n    |   └── __init__.py\n    ├── errors  # For every custom exception made\n    |   ├── core  # Make as many scripts as packages in core (i.e. processing.py for core.processing)\n    |   |   └── __init__.py\n    |   └── __init__.py\n    ├── utils  # For any kind of util used in the project\n    |   ├── logging\n    |   |   ├── __init__.py\n    |   |   └── handlers.yml  # For custom logging handles (i.e. database logging)\n    |   ├── __init__.py\n    |   └── helpers.py\n    └── __init__.py\ntests\n├── __init__.py\n└── example_test.py\n.gitignore\nLICENSE # Empty file\nREADME.md\nrequirements.txt\nsetup.py\n```\n\nThere are other PyBuilder plugins that depend on pybuilder_archetype_base that include other more specific packages.\nThese plugins are:\n\n* [pybuilder_archetype_api](https://github.com/yeuk0/pybuilder-archetype-api): For projects focused on web services\n* (WIP) ~~[pybuilder_archetype_db](https://github.com/yeuk0/pybuilder-archetype-db): For projects using databases~~\n\n## How to use pybuilder_archetype_base\n\n> **NOTICE**: This plugin only works on Windows due to its dependency with pybuilder_pycharm_workspace PyBuilder\n> plugin. Using this plugin in other OS shall not work properly. Multi-platform support soon.\n\nAdd plugin dependencies to your `build.py` (it requires [pybuilder_pycharm_workspace](https://github.com/yeuk0/pybuilder-pycharm-workspace)\nto work properly):\n\n```python\nuse_plugin(\'pypi:pybuilder_archetype_base\')\nuse_plugin(\'pypi:pybuilder_pycharm_workspace\')\n```\n\nConfigure the plugin within your `init` function:\n\n```python\n@init\ndef initialise(project):\n    project.set_property(\'project_base_path\', project_path)\n    project.set_property(\'pycharm_workspace_project_path\', project_path)\n```\n\nThis will tell the plugin which is the project location in the filesystem. `project_base_path` property value should be\n always the same. It is needed to inform `pycharm_workspace_project_path` too in order to get\n  pybuilder_pycharm_workspace working.\n\nLaunch the task with:\n\n```console\n(venv) C:\\Users\\foo\\PycharmProjects\\bar> pyb create_archetype_base\n```\n\n### `build.py` file recommended\n\nThis plugin doesn\'t include a `build.py` file due to there should be already one at the moment of the execution of `pyb`\ncommand. The following template can be used along this plugin. Modify as desired.\n\n```python\nfrom pathlib import Path\n\nfrom pybuilder.core import use_plugin, init, Author, before\n\n\nuse_plugin(\'python.core\')\nuse_plugin(\'python.distutils\')\nuse_plugin(\'python.flake8\')\nuse_plugin(\'python.unittest\')\n\nuse_plugin(\'pypi:pybuilder_pycharm_workspace\')\nuse_plugin(\'pypi:pybuilder_archetype_base\')\n\nproject_path = Path(__file__).resolve().parent\n\nname = project_path.name\nauthors = [Author("foo", \'bar\')]\nlicense = "Apache License, Version 2.0"\nversion = \'1.0.0\'\n\n\n@init\ndef initialise(project):\n    project.depends_on_requirements(\'requirements.txt\')\n\n    project.set_property(\'dir_source_main_python\', \'src\')\n\n    project.set_property(\'dir_source_unittest_python\', \'tests\')\n    project.set_property(\'unittest_module_glob\', \'test_*\')\n\n    project.set_property(\'project_base_path\', project_path)\n    project.set_property(\'pycharm_workspace_project_path\', project_path)\n\n\n@init(environments=\'develop\')\ndef initialise_dev(project):\n    project.version = f\'{project.version}.dev\'\n    project.set_property(\'flake8_verbose_output\', True)\n\n\n@init(environments=\'production\')\ndef initialise_pro(project):\n    project.set_property(\'flake8_break_build\', True)\n    project.set_property(\'flake8_include_test_sources\', True)\n\n\n@before(\'prepare\')\ndef pack_files(project):\n    """\n    Includes non-Python files in the build.\n\n    :param pybuilder.core.Project project: PyBuilder project instance\n    :return: None\n    """\n    package_path = list(Path(project.get_property(\'dir_source_main_python\')).glob(\'*\'))[0]\n    resources_paths = sorted(package_path.glob(\'**\'))[1:]\n    project.package_data.update(\n        { package_path.name: [str((path.relative_to(package_path) / \'*\').as_posix()) for path in resources_paths] })\n```\n\nTake note of ``build.py`` example on [pybuilder_pycharm_workspace](https://github.com/yeuk0/pybuilder-pycharm-workspace/blob/master/README.md)\nplugin README to cover its needs too.\n\n## Properties\n\nPlugin has next properties with provided defaults\n\n| Name | Type | Default Value | Description |\n| --- | --- | --- | --- |\n| project_base_path | Path | None | Project\'s path in filesystem (same as `build.py` file). Mandatory |\n',
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

        url = 'https://github.com/yeuk0/pybuilder-archetype-base',
        project_urls = {},

        scripts = [],
        packages = [
            'pybuilder_archetype_base',
            'pybuilder_archetype_base.resources',
            'pybuilder_archetype_base.resources.tests',
            'pybuilder_archetype_base.resources.utils.logging'
        ],
        namespace_packages = [],
        py_modules = [],
        entry_points = {},
        data_files = [],
        package_data = {
            'pybuilder_archetype_base': ['resources/*', 'resources/config/*', 'resources/config/logger/*', 'resources/tests/*', 'resources/utils/*', 'resources/utils/logging/*']
        },
        install_requires = [],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        python_requires = '',
        obsoletes = [],
    )
