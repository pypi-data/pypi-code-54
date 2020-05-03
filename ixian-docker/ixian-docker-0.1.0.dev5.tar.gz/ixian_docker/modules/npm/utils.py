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

import json
import re
from ixian.config import CONFIG

LOCAL_PACKAGE = re.compile(r"^file:(?P<var>.*)")


def get_package_json():
    with open(CONFIG.NPM.PACKAGE_JSON) as file:
        return json.loads(file.read())


def npm_local_packages():
    """
    Get list of local packages

    :return: a tuple of dicts
    """
    local_dependencies = {}
    local_dev_dependencies = {}
    package_json = get_package_json()
    for name, version in package_json.get("dependencies", {}).items():
        match = LOCAL_PACKAGE.match(version)
        if match:
            [local_dependencies[name]] = match.groups()
    for name, version in package_json.get("devDependencies", {}).items():
        match = LOCAL_PACKAGE.match(version)
        if match:
            [local_dev_dependencies[name]] = match.groups()
    return local_dependencies, local_dev_dependencies


def npm_local_package_mount_flags():
    """
    Creates docker flags to mount local packages in a docker builder. This
    allows local packages to be installed by `docker.build_library`.

    NPM only installs local packages with symlinks, so the library must also
    be mounted when used (e.g. when building with webpack)

    :return: a list of mount flags to pass to `docker.build_library`
    """

    # mount volumes in same directory as host so package.json works there too.
    volumes = []
    dependencies, dev_dependencies = npm_local_packages()
    for name, local_path in dependencies.items():
        volumes.append("{path}:{path}".format(path=local_path))
    for name, local_path in dev_dependencies.items():
        volumes.append("{path}:{path}".format(path=local_path))

    return volumes
