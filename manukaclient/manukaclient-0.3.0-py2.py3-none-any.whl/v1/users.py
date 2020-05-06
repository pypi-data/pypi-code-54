#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

import json

from manukaclient import base


class User(base.Resource):
    pass


class UserManager(base.BasicManager):

    base_url = 'v1/users'
    resource_class = User

    def update(self, user_id, **kwargs):
        data = json.dumps(kwargs)
        return self._update('/%s/%s/' % (self.base_url, user_id), data=data,
                            headers={"content-type": "application/json"})

    def get_by_os(self, user_id):
        return self._get('v1/users-os/%s/' % user_id)

    def search(self, query):
        return self._search('/%s/search/' % self.base_url,
                            data={'search': query})
