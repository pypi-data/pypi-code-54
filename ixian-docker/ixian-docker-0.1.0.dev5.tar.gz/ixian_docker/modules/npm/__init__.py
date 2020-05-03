# Copyright [2018-2020] Peter Krenesky
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


class NPMModuleConfig(object):
    """Custom config object for NPM module.

    Custom config to enable dynamically generated `dev_volumes`
    """

    name = "NPM"
    tasks = "ixian_docker.modules.npm.tasks"
    config = "ixian_docker.modules.npm.config.NPMConfig"
    dockerfile_template = "{NPM.DOCKERFILE_TEMPLATE}"

    def __getitem__(self, key):
        try:
            return getattr(self, key)
        except AttributeError:
            if key == "dev_volumes":
                return self.dev_volumes
            else:
                raise KeyError(key)

    def __contains__(self, key):
        return key in self.__dict__ or key == "dev_volumes"

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    @property
    def dev_volumes(self):
        from ixian_docker.modules.npm.utils import npm_local_package_mount_flags

        return npm_local_package_mount_flags()


OPTIONS = NPMModuleConfig()
