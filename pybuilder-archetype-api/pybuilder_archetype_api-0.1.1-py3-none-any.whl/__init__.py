#   -*- coding: utf-8 -*-
#   Copyright 2020 Arturo González, Diego Barrantes
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from pathlib import Path

from pybuilder.core import depends, init, task
from pybuilder_archetype_api.helpers import BuilderAPI
from pybuilder_archetype_base.helpers import Utils

import pybuilder_archetype_api.messages as msg
import pybuilder_archetype_base.messages as msg_base


@init
def initialise_plugin(project):
	"""
	Sets project defaults.

	:param pybuilder.core.Project project: PyBuilder project instance
	:return: None
	"""
	directories = {
		'SRC': Path('src')
	}
	project.set_property('api_directories', directories)

	packages = {
		'MAIN': Path('.'),
		'API': Path('api'),
		'CONFIG': Path('config')
	}
	project.set_property('api_packages', packages)

	templates_first_level = {
		'REQUIREMENTS': 'requirements.txt'
	}
	project.set_property('api_templates_first_level', templates_first_level)

	templates_second_level = {
		'API_EXAMPLE': packages['API'] / 'api_example.py',
		'GUNICORN_CONFIG': packages['MAIN'] / 'gunicorn_config.py',
		'MAIN': packages['MAIN'] / 'main.py',
		'CONFIG_CONSTANTS': packages['CONFIG'] / 'constants.py',
		'WSGI': packages['MAIN'] / 'wsgi.py'
	}
	project.set_property('api_templates_second_level', templates_second_level)


@task(description=msg.TASK_DESCRIPTION_CREATE_ARCHETYPE_API)
@depends('create_archetype_base')
def create_archetype_api(project, logger):
	"""
	Main plugin task.

	It creates the project skeleton for a web service. It depends on ``create_archetype_base`` task that will set project base structure.

	:param pybuilder.core.Project project: PyBuilder project instance
	:param pybuilder.core.Logger logger: PyBuilder logger instance
	:return: None
	"""
	logger.info(msg.ARCHETYPE_START)

	builder = BuilderAPI(logger)
	project_path = Path(Utils.underscore(project.name))

	logger.info(msg_base.ARCHETYPE_DIRECTORIES)
	for directory in project.get_property('api_directories').values():
		builder.create_directory(project_path, directory, False)

	logger.info(msg_base.ARCHETYPE_PACKAGES)
	for package in project.get_property('api_packages').values():
		builder.create_directory(project_path, package, True)

	logger.info(msg_base.ARCHETYPE_TEMPLATES_ROOT)
	for template in project.get_property('api_templates_first_level').values():
		builder.copy_file_templates(Path('.'), Path(__file__).parent, template, [project.get_property('api_templates_first_level')['REQUIREMENTS']])

	logger.info(msg_base.ARCHETYPE_TEMPLATES_PACKAGE)
	for template in project.get_property('api_templates_second_level').values():
		builder.copy_file_templates('src' / project_path, Path(__file__).parent, template, [project.get_property('api_templates_second_level')['CONFIG_CONSTANTS'].name])

	logger.info(msg_base.ARCHETYPE_INIT_FILE)
	for package in project.get_property('api_packages').values():
		builder.create_init(project_path, Path(__file__).parent, package)

	logger.info(msg.ARCHETYPE_FINISH)
