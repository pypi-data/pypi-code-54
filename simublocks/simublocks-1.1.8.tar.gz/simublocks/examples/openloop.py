openloop = {
    "name": "open.json",
    "importCode": "",
    "blocks": {
        "1": {
            "name": "Input",
            "type": "input",
            "conn": [
                {},
                {
                    "otherblock": "Sys (TF)",
                    "otherblock_n_arc": 0,
                    "otherblock_id": 2
                },
                {}
            ],
            "code": "def Input(t,k):\n\tif t < 15:\n\t\treturn 1\n\telse:\n\t\treturn 3\n",
            "coords": [
                50,
                50,
                150,
                150
            ]
        },
        "2": {
            "name": "Sys (TF)",
            "type": "system",
            "conn": [
                {
                    "otherblock": "Input",
                    "otherblock_n_arc": 1,
                    "otherblock_id": 1
                },
                {},
                {}
            ],
            "code": {
                "type": "TF",
                "sub_type": "continuous",
                "self": [
                    "[1]",
                    "[1,2,3]"
                ]
            },
            "coords": [
                301.0,
                50.0,
                401.0,
                150.0
            ]
        }
    },
    "graphs": {
        "3": {
            "name": "Graph",
            "type": "graph",
            "conn": [
                {},
                {},
                {}
            ],
            "code": [
                {
                    "name": "Input",
                    "type": "input",
                    "subtype": "output",
                    "legend": "input",
                    "color": "red",
                    "check": True
                }
            ],
            "coords": [
                507.0,
                190.0,
                607.0,
                290.0
            ]
        },
        "4": {
            "name": "Graph",
            "type": "graph",
            "conn": [
                {},
                {},
                {}
            ],
            "code": [
                {
                    "name": "Sys (TF)",
                    "type": "system",
                    "subtype": "output",
                    "legend": "output",
                    "color": "blue",
                    "check": True
                }
            ],
            "coords": [
                510.0,
                33.0,
                610.0,
                133.0
            ]
        }
    }
}