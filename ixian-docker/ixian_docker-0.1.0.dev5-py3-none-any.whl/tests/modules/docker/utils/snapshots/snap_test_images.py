# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from pysnap import Snapshot


snapshots = Snapshot()

snapshots['TestPush.test_push 1'] = '''The push refers to repository [896552222739.dkr.ecr.us-west-2.amazonaws.com/lims/testing]
77cae8ab23bf: Preparing \x1b[K\r77cae8ab23bf: Pushing [>                                                  ]  68.61kB/5.553MB\x1b[K\r77cae8ab23bf: Pushing [====>                                              ]  461.8kB/5.553MB\x1b[K\r77cae8ab23bf: Pushing [=======>                                           ]  845.3kB/5.553MB\x1b[K\r77cae8ab23bf: Pushing [==================>                                ]  2.055MB/5.553MB\x1b[K\r77cae8ab23bf: Pushing [====================>                              ]  2.251MB/5.553MB\x1b[K\r77cae8ab23bf: Pushing [===============================>                   ]  3.496MB/5.553MB\x1b[K\r77cae8ab23bf: Pushing [==========================================>        ]  4.694MB/5.553MB\x1b[K\r77cae8ab23bf: Pushing [==================================================>]  5.815MB\x1b[K\r77cae8ab23bf: Pushed \x1b[K\rpush_test: digest: sha256:e4355b66995c96b4b468159fc5c7e3540fcef961189ca13fee877798649f531a size: 528
'''

snapshots['TestPush.test_push_already_pushed 1'] = '''The push refers to repository [896552222739.dkr.ecr.us-west-2.amazonaws.com/lims/testing]
77cae8ab23bf: Preparing \x1b[K\r77cae8ab23bf: Layer already exists \x1b[K\rpush_test: digest: sha256:e4355b66995c96b4b468159fc5c7e3540fcef961189ca13fee877798649f531a size: 528
'''

snapshots['TestPush.test_push_tag 1'] = '''The push refers to repository [896552222739.dkr.ecr.us-west-2.amazonaws.com/lims/testing]
77cae8ab23bf: Preparing \x1b[K\r77cae8ab23bf: Pushing [>                                                  ]  68.61kB/5.553MB\x1b[K\r77cae8ab23bf: Pushing [====>                                              ]  461.8kB/5.553MB\x1b[K\r77cae8ab23bf: Pushing [=======>                                           ]  845.3kB/5.553MB\x1b[K\r77cae8ab23bf: Pushing [==================>                                ]  2.055MB/5.553MB\x1b[K\r77cae8ab23bf: Pushing [====================>                              ]  2.251MB/5.553MB\x1b[K\r77cae8ab23bf: Pushing [===============================>                   ]  3.496MB/5.553MB\x1b[K\r77cae8ab23bf: Pushing [==========================================>        ]  4.694MB/5.553MB\x1b[K\r77cae8ab23bf: Pushing [==================================================>]  5.815MB\x1b[K\r77cae8ab23bf: Pushed \x1b[K\rpush_test: digest: sha256:e4355b66995c96b4b468159fc5c7e3540fcef961189ca13fee877798649f531a size: 528
'''

snapshots['TestPush.test_push_silent 1'] = ''

snapshots['TestPull.test_pull 1'] = '''Using default tag: latest
latest: Pulling from library/alpine \x1b[K\r
89d9c30c1d48: Pulling fs layer \x1b[K\r89d9c30c1d48: Downloading [>                                                  ]  28.02kB/2.787MB\x1b[K\r89d9c30c1d48: Downloading [=====================>                             ]  1.178MB/2.787MB\x1b[K\r89d9c30c1d48: Downloading [=========================================>         ]  2.309MB/2.787MB\x1b[K\r89d9c30c1d48: Verifying Checksum \x1b[K\r89d9c30c1d48: Download complete \x1b[K\r89d9c30c1d48: Extracting [>                                                  ]  32.77kB/2.787MB\x1b[K\r89d9c30c1d48: Extracting [======>                                            ]  360.4kB/2.787MB\x1b[K\r89d9c30c1d48: Extracting [==================================================>]  2.787MB/2.787MB\x1b[K\r89d9c30c1d48: Pull complete \x1b[K\r\x1b[1B\rDigest: sha256:c19173c5ada610a5989151111163d28a67368362762534d8a8121ce95cf2bd5a
Status: Downloaded newer image for alpine:latest
ixian_docker.test:latest
'''

snapshots['TestPull.test_pull_silent 1'] = '''ixian_docker.test:latest
'''

snapshots['TestPull.test_pull_tag 1'] = '''latest: Pulling from library/alpine \x1b[K\r
89d9c30c1d48: Pulling fs layer \x1b[K\r89d9c30c1d48: Downloading [>                                                  ]  28.02kB/2.787MB\x1b[K\r89d9c30c1d48: Downloading [=====================>                             ]  1.178MB/2.787MB\x1b[K\r89d9c30c1d48: Downloading [=========================================>         ]  2.309MB/2.787MB\x1b[K\r89d9c30c1d48: Verifying Checksum \x1b[K\r89d9c30c1d48: Download complete \x1b[K\r89d9c30c1d48: Extracting [>                                                  ]  32.77kB/2.787MB\x1b[K\r89d9c30c1d48: Extracting [======>                                            ]  360.4kB/2.787MB\x1b[K\r89d9c30c1d48: Extracting [==================================================>]  2.787MB/2.787MB\x1b[K\r89d9c30c1d48: Pull complete \x1b[K\r\x1b[1B\rDigest: sha256:c19173c5ada610a5989151111163d28a67368362762534d8a8121ce95cf2bd5a
Status: Downloaded newer image for alpine:latest
ixian_docker.test:custom_tag
'''

snapshots['TestPush.test_push_error 1'] = '''The push refers to repository [FAKE.dkr.ecr.us-west-2.amazonaws.com/testing]
77cae8ab23bf: Preparing \x1b[K\r'''

snapshots['TestPush.test_push_error_and_silent 1'] = ''
