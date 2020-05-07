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
from shutil import copy

import pybuilder_archetype_api.messages as msg
import pybuilder_archetype_base.messages as msg_base
from pybuilder_archetype_base.helpers import Builder, Utils


class BuilderAPI(Builder):
	"""
	Class to support project structure building.

	``BuilderAPI`` class offers methods to create new Python packages and directories as well as copy file templates to
	new project location. It extends from ``Builder`` class defined in pybuilder_archetype_base module.
	"""

	def copy_file_templates(self, project_package, template_source, directory_path, to_update=[]):
		"""
		Copies a template file to a specific location.

		This method takes into consideration the files that were created by base plugin and modifies them.

		:param Path project_package: Name of project's main package
		:param Path template_source: Path where the template is located
		:param str or Path directory_path: Directory where the file will be copied
		:param list[str] to_update: Collection of file names that will be updated (not created). Default: []
		:return: None
		"""
		file_path = project_package / directory_path
		path_from_file = template_source / 'resources' / directory_path
		if file_path.exists():
			if Path(directory_path).name not in to_update:
				self.logger.debug(msg_base.BUILDER_FILE_EXISTS.format(file=file_path))
				return

			if 'requirements.txt' is directory_path:
				Utils.update_requirements(path_from_file, file_path)
			else:
				Utils.update_file(path_from_file, file_path)
			self.logger.debug(msg.BUILDER_FILE_UPDATED.format(file=file_path))
		else:
			copy(path_from_file, file_path)
			self.logger.debug(msg_base.BUILDER_FILE_CREATED.format(file=file_path))
