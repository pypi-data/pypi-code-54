"""Copyright 2019 Cisco Systems
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

 * Redistributions of source code must retain the above copyright
 notice, this list of conditions and the following disclaimer.

The contents of this file are licensed under the Apache License, Version 2.0
(the "License"); you may not use this file except in compliance with the
License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations under
the License.
"""

import grpc


class CiscoAuthPlugin(grpc.AuthMetadataPlugin):
    """A gRPC AuthMetadataPlugin which adds username/password metadata to each call."""

    def __init__(self, username, password):
        super(CiscoAuthPlugin, self).__init__()
        self.username = username
        self.password = password

    def __call__(self, context, callback):
        callback([("username", self.username), ("password", self.password)], None)
