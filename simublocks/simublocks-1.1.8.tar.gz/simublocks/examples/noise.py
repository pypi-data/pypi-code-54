noise_example = {
    "name": "noise.json",
    "importCode": "import numpy as np\n\nnoise_vector= np.random.normal(0, 0.05, size=50000)\n\n",
    "blocks": {
        "1": {
            "name": "input",
            "type": "input",
            "conn": [
                {},
                {
                    "otherblock": "system",
                    "otherblock_n_arc": 0,
                    "otherblock_id": 2
                },
                {}
            ],
            "code": "def input(t,k):\n\tif t < 15:\n\t\treturn 1\n\telse:\n\t\treturn 3\n\n",
            "coords": [
                50,
                50,
                150,
                150
            ]
        },
        "2": {
            "name": "system",
            "type": "system",
            "conn": [
                {
                    "otherblock": "input",
                    "otherblock_n_arc": 1,
                    "otherblock_id": 1
                },
                {
                    "otherblock": "Sum6",
                    "otherblock_n_arc": 0,
                    "otherblock_id": 4
                },
                {}
            ],
            "code": {
                "type": "TF",
                "sub_type": "continuous",
                "self": [
                    "[1]",
                    "[1,4,3]"
                ]
            },
            "coords": [
                301.0,
                50.0,
                401.0,
                150.0
            ]
        },
        "3": {
            "name": "noise",
            "type": "input",
            "conn": [
                {},
                {
                    "otherblock": "",
                    "otherblock_n_arc": 0,
                    "otherblock_id": 5
                },
                {}
            ],
            "code": "def noise(t,k):\n\treturn noise_vector[k]\n\n# Please, look at Other > Import Code\n\n",
            "coords": [
                212.0,
                248.0,
                312.0,
                348.0
            ]
        },
        "4": {
            "name": "Sum6",
            "type": "sum",
            "conn": [
                {
                    "otherblock": "system",
                    "otherblock_n_arc": 1,
                    "otherblock_id": 2
                },
                {
                    "otherblock": "filter",
                    "otherblock_n_arc": 0,
                    "otherblock_id": 7
                },
                {
                    "otherblock": "",
                    "otherblock_n_arc": 1,
                    "otherblock_id": 5
                }
            ],
            "code": [
                "+",
                "+"
            ],
            "coords": [
                503.0,
                76.0,
                553.0,
                126.0
            ]
        },
        "5": {
            "name": "",
            "type": "corner",
            "conn": [
                {
                    "otherblock": "noise",
                    "otherblock_n_arc": 1,
                    "otherblock_id": 3
                },
                {
                    "otherblock": "Sum6",
                    "otherblock_n_arc": 2,
                    "otherblock_id": 4
                },
                {}
            ],
            "code": [
                "left",
                "top"
            ],
            "coords": [
                514.0,
                283.0,
                544.0,
                313.0
            ]
        },
        "7": {
            "name": "filter",
            "type": "system",
            "conn": [
                {
                    "otherblock": "Sum6",
                    "otherblock_n_arc": 1,
                    "otherblock_id": 4
                },
                {},
                {}
            ],
            "code": {
                "type": "TF",
                "sub_type": "continuous",
                "self": [
                    "[1]",
                    "[0.1,1]"
                ]
            },
            "coords": [
                688.0,
                51.0,
                788.0,
                151.0
            ]
        }
    },
    "graphs": {
        "6": {
            "name": "Graph",
            "type": "graph",
            "conn": [
                {},
                {},
                {}
            ],
            "code": [
                {
                    "name": "Sum6",
                    "type": "sum",
                    "legend": "system output",
                    "color": "",
                    "check": True
                },
                {
                    "name": "filter",
                    "type": "system",
                    "legend": "filter output",
                    "color": "",
                    "check": True
                }
            ],
            "coords": [
                681.0,
                306.0,
                781.0,
                406.0
            ]
        }
    }
}