PULL_SUCCESSFUL = [
    {"status": "Pulling from library/alpine", "id": "latest"},
    {"status": "Pulling fs layer", "progressDetail": {}, "id": "89d9c30c1d48"},
    {
        "status": "Downloading",
        "progressDetail": {"current": 28018, "total": 2787134},
        "progress": "[>                                                  ]  28.02kB/2.787MB",
        "id": "89d9c30c1d48",
    },
    {
        "status": "Downloading",
        "progressDetail": {"current": 1178287, "total": 2787134},
        "progress": "[=====================>                             ]  1.178MB/2.787MB",
        "id": "89d9c30c1d48",
    },
    {
        "status": "Downloading",
        "progressDetail": {"current": 2308783, "total": 2787134},
        "progress": "[=========================================>         ]  2.309MB/2.787MB",
        "id": "89d9c30c1d48",
    },
    {"status": "Verifying Checksum", "progressDetail": {}, "id": "89d9c30c1d48"},
    {"status": "Download complete", "progressDetail": {}, "id": "89d9c30c1d48"},
    {
        "status": "Extracting",
        "progressDetail": {"current": 32768, "total": 2787134},
        "progress": "[>                                                  ]  32.77kB/2.787MB",
        "id": "89d9c30c1d48",
    },
    {
        "status": "Extracting",
        "progressDetail": {"current": 360448, "total": 2787134},
        "progress": "[======>                                            ]  360.4kB/2.787MB",
        "id": "89d9c30c1d48",
    },
    {
        "status": "Extracting",
        "progressDetail": {"current": 2787134, "total": 2787134},
        "progress": "[==================================================>]  2.787MB/2.787MB",
        "id": "89d9c30c1d48",
    },
    {"status": "Pull complete", "progressDetail": {}, "id": "89d9c30c1d48"},
    {
        "status": "Digest: sha256:c19173c5ada610a5989151111163d28a67368362762534d8a8121ce95cf2bd5a"
    },
    {"status": "Status: Downloaded newer image for alpine:latest"},
]
PULL_ALREADY_PRESENT = [
    {"status": "Pulling from library/alpine", "id": "latest"},
    {
        "status": "Digest: sha256:c19173c5ada610a5989151111163d28a67368362762534d8a8121ce95cf2bd5a"
    },
    {"status": "Status: Image is up to date for alpine:latest"},
]

PUSH_SUCCESSFUL = [
    {
        "status": "The push refers to repository [896552222739.dkr.ecr.us-west-2.amazonaws.com/lims/testing]"
    },
    {"status": "Preparing", "progressDetail": {}, "id": "77cae8ab23bf"},
    {
        "status": "Pushing",
        "progressDetail": {"current": 68608, "total": 5552690},
        "progress": "[>                                                  ]  68.61kB/5.553MB",
        "id": "77cae8ab23bf",
    },
    {
        "status": "Pushing",
        "progressDetail": {"current": 461824, "total": 5552690},
        "progress": "[====>                                              ]  461.8kB/5.553MB",
        "id": "77cae8ab23bf",
    },
    {
        "status": "Pushing",
        "progressDetail": {"current": 845312, "total": 5552690},
        "progress": "[=======>                                           ]  845.3kB/5.553MB",
        "id": "77cae8ab23bf",
    },
    {
        "status": "Pushing",
        "progressDetail": {"current": 2054656, "total": 5552690},
        "progress": "[==================>                                ]  2.055MB/5.553MB",
        "id": "77cae8ab23bf",
    },
    {
        "status": "Pushing",
        "progressDetail": {"current": 2251264, "total": 5552690},
        "progress": "[====================>                              ]  2.251MB/5.553MB",
        "id": "77cae8ab23bf",
    },
    {
        "status": "Pushing",
        "progressDetail": {"current": 3496448, "total": 5552690},
        "progress": "[===============================>                   ]  3.496MB/5.553MB",
        "id": "77cae8ab23bf",
    },
    {
        "status": "Pushing",
        "progressDetail": {"current": 4693504, "total": 5552690},
        "progress": "[==========================================>        ]  4.694MB/5.553MB",
        "id": "77cae8ab23bf",
    },
    {
        "status": "Pushing",
        "progressDetail": {"current": 5814784, "total": 5552690},
        "progress": "[==================================================>]  5.815MB",
        "id": "77cae8ab23bf",
    },
    {"status": "Pushed", "progressDetail": {}, "id": "77cae8ab23bf"},
    {
        "status": "push_test: digest: sha256:e4355b66995c96b4b468159fc5c7e3540fcef961189ca13fee877798649f531a size: 528"
    },
    {
        "progressDetail": {},
        "aux": {
            "Tag": "push_test",
            "Digest": "sha256:e4355b66995c96b4b468159fc5c7e3540fcef961189ca13fee877798649f531a",
            "Size": 528,
        },
    },
]
PUSH_SUCCESSFUL_CUSTOM_TAG = PUSH_SUCCESSFUL
PUSH_ALREADY_PRESENT = [
    {
        "status": "The push refers to repository [896552222739.dkr.ecr.us-west-2.amazonaws.com/lims/testing]"
    },
    {"status": "Preparing", "progressDetail": {}, "id": "77cae8ab23bf"},
    {"status": "Layer already exists", "progressDetail": {}, "id": "77cae8ab23bf"},
    {
        "status": "push_test: digest: sha256:e4355b66995c96b4b468159fc5c7e3540fcef961189ca13fee877798649f531a size: 528"
    },
    {
        "progressDetail": {},
        "aux": {
            "Tag": "push_test",
            "Digest": "sha256:e4355b66995c96b4b468159fc5c7e3540fcef961189ca13fee877798649f531a",
            "Size": 528,
        },
    },
]

ECR_PUSH_AUTH_FAILURE = [
    {
        "status": "The push refers to repository [FAKE.dkr.ecr.us-west-2.amazonaws.com/testing]"
    },
    {"status": "Preparing", "progressDetail": {}, "id": "77cae8ab23bf"},
    {
        "errorDetail": {
            "message": "denied: Your Authorization Token has expired. Please run 'aws ecr get-login --no-include-email' to fetch a new one."
        },
        "error": "denied: Your Authorization Token has expired. Please run 'aws ecr get-login --no-include-email' to fetch a new one.",
    },
]
