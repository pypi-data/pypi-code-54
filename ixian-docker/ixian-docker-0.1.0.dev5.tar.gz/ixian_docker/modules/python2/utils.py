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

from itertools import chain
from pipenv.patched.pipfile.api import PipfileParser


def pipenv_local_package_mount_flags():
    """
    Reads Pipfile and returns a list of paths for all locally installed
    packages.

    Returns:
        List of filesystem paths.
    """

    from ixian.config import CONFIG

    pipfile = PipfileParser(CONFIG.PYTHON.PIPFILE)
    data = pipfile.parse()

    flags = []
    items = chain(data["default"].items(), data["develop"].items())
    for package, datum in items:
        if isinstance(datum, dict) and datum.get("editable", False):
            flags.append("{path}:{path}".format(**datum))
    return flags
