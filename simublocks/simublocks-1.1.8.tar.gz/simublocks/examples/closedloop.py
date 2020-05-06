closedloop = {
    "name": "closed.json",
    "importCode": "",
    "blocks": {
        "1": {
            "name": "Sum1",
            "type": "sum",
            "conn": [
                {
                    "otherblock": "SetPoint",
                    "otherblock_n_arc": 1,
                    "otherblock_id": 9
                },
                {
                    "otherblock": "PI (SS)",
                    "otherblock_n_arc": 0,
                    "otherblock_id": 6
                },
                {
                    "otherblock": "",
                    "otherblock_n_arc": 1,
                    "otherblock_id": 5
                }
            ],
            "code": [
                "+",
                "-"
            ],
            "coords": [
                228.0,
                87.0,
                278.0,
                137.0
            ]
        },
        "2": {
            "name": "Sys (TF)",
            "type": "system",
            "conn": [
                {
                    "otherblock": "Sum2",
                    "otherblock_n_arc": 1,
                    "otherblock_id": 7
                },
                {
                    "otherblock": "",
                    "otherblock_n_arc": 0,
                    "otherblock_id": 4
                },
                {}
            ],
            "code": {
                "type": "TF",
                "sub_type": "continuous",
                "self": [
                    "[25]",
                    "[1,5,25]"
                ]
            },
            "coords": [
                581.0,
                62.0,
                681.0,
                162.0
            ]
        },
        "3": {
            "name": "",
            "type": "corner",
            "conn": [
                {
                    "otherblock": "",
                    "otherblock_n_arc": 1,
                    "otherblock_id": 4
                },
                {
                    "otherblock": "",
                    "otherblock_n_arc": 0,
                    "otherblock_id": 5
                },
                {}
            ],
            "code": [
                "top",
                "left"
            ],
            "coords": [
                755.0,
                304.0,
                785.0,
                334.0
            ]
        },
        "4": {
            "name": "",
            "type": "corner",
            "conn": [
                {
                    "otherblock": "Sys (TF)",
                    "otherblock_n_arc": 1,
                    "otherblock_id": 2
                },
                {
                    "otherblock": "",
                    "otherblock_n_arc": 0,
                    "otherblock_id": 3
                },
                {}
            ],
            "code": [
                "left",
                "bottom"
            ],
            "coords": [
                754.0,
                97.0,
                784.0,
                127.0
            ]
        },
        "5": {
            "name": "",
            "type": "corner",
            "conn": [
                {
                    "otherblock": "",
                    "otherblock_n_arc": 1,
                    "otherblock_id": 3
                },
                {
                    "otherblock": "Sum1",
                    "otherblock_n_arc": 2,
                    "otherblock_id": 1
                },
                {}
            ],
            "code": [
                "right",
                "top"
            ],
            "coords": [
                239.0,
                303.0,
                269.0,
                333.0
            ]
        },
        "6": {
            "name": "PI (SS)",
            "type": "system",
            "conn": [
                {
                    "otherblock": "Sum1",
                    "otherblock_n_arc": 1,
                    "otherblock_id": 1
                },
                {
                    "otherblock": "Sum2",
                    "otherblock_n_arc": 0,
                    "otherblock_id": 7
                },
                {}
            ],
            "code": {
                "type": "SS",
                "sub_type": "discrete",
                "self": [
                    "[ 1 ]",
                    "[1]",
                    "[0.05]",
                    "[1]"
                ]
            },
            "coords": [
                341.0,
                62.0,
                441.0,
                162.0
            ]
        },
        "7": {
            "name": "Sum2",
            "type": "sum",
            "conn": [
                {
                    "otherblock": "PI (SS)",
                    "otherblock_n_arc": 1,
                    "otherblock_id": 6
                },
                {
                    "otherblock": "Sys (TF)",
                    "otherblock_n_arc": 0,
                    "otherblock_id": 2
                },
                {
                    "otherblock": "",
                    "otherblock_n_arc": 1,
                    "otherblock_id": 8
                }
            ],
            "code": [
                "+",
                "+"
            ],
            "coords": [
                486.0,
                88.0,
                536.0,
                138.0
            ]
        },
        "8": {
            "name": "",
            "type": "corner",
            "conn": [
                {
                    "otherblock": "Disturbance",
                    "otherblock_n_arc": 1,
                    "otherblock_id": 10
                },
                {
                    "otherblock": "Sum2",
                    "otherblock_n_arc": 2,
                    "otherblock_id": 7
                },
                {}
            ],
            "code": [
                "left",
                "top"
            ],
            "coords": [
                497.0,
                218.0,
                527.0,
                248.0
            ]
        },
        "9": {
            "name": "SetPoint",
            "type": "input",
            "conn": [
                {},
                {
                    "otherblock": "Sum1",
                    "otherblock_n_arc": 0,
                    "otherblock_id": 1
                },
                {}
            ],
            "code": "def SetPoint(t,k):\n\tif t < 10:\n\t\treturn 10\n\telse:\n\t\treturn 30\n\n",
            "coords": [
                57.0,
                62.0,
                157.0,
                162.0
            ]
        },
        "10": {
            "name": "Disturbance",
            "type": "input",
            "conn": [
                {},
                {
                    "otherblock": "",
                    "otherblock_n_arc": 0,
                    "otherblock_id": 8
                },
                {}
            ],
            "code": "def Disturbance(t,k):\n\tif t < 20:\n\t\treturn 0\n\telse:\n\t\treturn 5\n\n\n\n\n\n\n",
            "coords": [
                301.0,
                184.0,
                401.0,
                284.0
            ]
        }
    },
    "graphs": {
        "11": {
            "name": "Graph",
            "type": "graph",
            "conn": [
                {},
                {},
                {}
            ],
            "code": [
                {
                    "name": "PI (SS)",
                    "type": "system",
                    "legend": "PI control signal",
                    "color": "b--",
                    "check": True
                },
                {
                    "name": "Sum2",
                    "type": "sum",
                    "legend": "disturbed control signal",
                    "color": "r",
                    "check": True
                },
                {
                    "name": "Disturbance",
                    "type": "input",
                    "legend": "disturbance signal",
                    "color": "k",
                    "check": True
                }
            ],
            "coords": [
                862.0,
                46.0,
                962.0,
                146.0
            ]
        },
        "12": {
            "name": "Graph",
            "type": "graph",
            "conn": [
                {},
                {},
                {}
            ],
            "code": [
                {
                    "name": "Sum1",
                    "type": "sum",
                    "legend": "error",
                    "color": "",
                    "check": True
                },
                {
                    "name": "Sys (TF)",
                    "type": "system",
                    "legend": "output",
                    "color": "",
                    "check": True
                },
                {
                    "name": "SetPoint",
                    "type": "input",
                    "legend": "setpoint",
                    "color": "k--",
                    "check": True
                }
            ],
            "coords": [
                852.0,
                174.0,
                952.0,
                274.0
            ]
        }
    }
}