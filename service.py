from flask import Flask, send_file
from flask_restful import Resource, Api
from flask_cors import CORS
from storageFunctions import ValidateFileExist, ValidateFileName, WriteToPublic, GetTextFromPublic, GetFileNamesInFolder

# Setup
app = Flask(__name__)
api = Api(app)
CORS(app)

# The "/" endpoint
class Root(Resource):
    def get(self):
        return "I am (g)root"

# The "/info" endpoint
class Info(Resource):
    def get(self):
        return {
            "id": "NN-Service",
            "name": "NN time-series predictions",
            "version": "2020v1",
            "category": 2,
            "input": [{
                "name": "data-input",
                "label": "Input data",
                "type": "time-series"
            }],
            "output": [{
                "name": "data-output",
                "label": "Output data",
                "type": "time-series"
            }]
        }

# The "/fields" endpoint
class Fields(Resource):
    def get(self):
        return {
            "user_fields": [
                {
                    "name": "dataset",
                    "label": "Dataset",
                    "placeholder": "See documentation for format",
                    "type": "file"
                },
                {
                    "name": "preset",
                    "label": "Param preset",
                    "default": "p1",
                    "type": "select",
                    "options": [ 
                        {
                            "name": "Preset1",
                            "value": "p1"
                        },
                        {
                            "name": "Preset2",
                            "value": "p2"
                        },
                        {
                            "name": "Manual-mode",
                            "value": "m"
                        }  
                    ]
                },
                {
                    "name": "hidCNN",
                    "label": "CNN hidden units",
                    "placeholder": "(Only used in manual-mode)",
                    "type": "input-number"
                },
                {
                    "name": "hidRNN",
                    "label": "RNN hidden units",
                    "placeholder": "(Only used in manual-mode)",
                    "type": "input-number"
                },
                {
                    "name": "window",
                    "label": "Window size",
                    "placeholder": "(Only used in manual-mode)",
                    "type": "input-number"
                },
                {
                    "name": "CNN_kernel",
                    "label": "CNN Kernel size",
                    "placeholder": "(Only used in manual-mode)",
                    "type": "input-number"
                },
                {
                    "name": "highway_window",
                    "label": "Window size of highway component",
                    "placeholder": "(Only used in manual-mode)",
                    "type": "input-number"
                },
                {
                    "name": "clip",
                    "label": "Gradient clipping",
                    "placeholder": "(Only used in manual-mode)",
                    "type": "input-number"
                },
                {
                    "name": "epochs",
                    "label": "Upper epoch limit",
                    "placeholder": "(Only used in manual-mode)",
                    "type": "input-number"
                },
                {
                    "name": "batch_size",
                    "label": "Batch size",
                    "placeholder": "(Only used in manual-mode)",
                    "type": "input-number"
                },
                {
                    "name": "dropout",
                    "label": "Dropout applied to layers",
                    "placeholder": "(Only used in manual-mode)",
                    "type": "input-number"
                },
                {
                    "name": "seed",
                    "label": "Random seed",
                    "placeholder": "(Only used in manual-mode)",
                    "type": "input-number"
                }
            ],
            "developer_fields": [
                {
                    "name": "preset",
                    "label": "Param preset",
                    "default": "p1",
                    "type": "select",
                    "options": [ 
                        {
                            "name": "Preset1",
                            "value": "p1"
                        },
                        {
                            "name": "Preset2",
                            "value": "p2"
                        }
                    ]
                }
            ]
        }

# The "/readme" endpoint
class Readme(Resource):
    def get(self):
        return {
            "chart_type": "markdown",
            "content": GetTextFromPublic("", "documentation.md")
        }

# The "/render" endpoint
class Render(Resource):
    def post(self):
        return {
          'chart_type': 'time-series-data',
          'content': {
            "settings": {
              "to_chart": "generic-time-series",
              "predictions": [
                [
                  {
                    'data': [
                      2,
                      2,
                      2
                    ],
                    'error': {
                      'mae': 5,
                      'smape': 6
                    }
                  },
                  {
                    'data': [
                      3,
                      3,
                      3
                    ],
                    'error': {
                      'mae': 5,
                      'smape': 6
                    }
                  },
                  {
                    'data': [
                      4,
                      4,
                      4
                    ],
                    'error': {
                      'mae': 5,
                      'smape': 6
                    }
                  },
                  {
                    'data': [
                      5,
                      5,
                      5
                    ],
                    'error': {
                      'mae': 5,
                      'smape': 6
                    }
                  },
                  {
                    'data': [
                      6,
                      6,
                      6
                    ],
                    'error': {
                      'mae': 5,
                      'smape': 6
                    }
                  },
                  {
                    'data': [
                      7,
                      7,
                      7
                    ],
                    'error': {
                      'mae': 5,
                      'smape': 6
                    }
                  },
                  {
                    'data': [
                      7,
                      7,
                      7
                    ],
                    'error': {
                      'mae': 5,
                      'smape': 6
                    }
                  },
                  {
                    'data': [
                      7,
                      7,
                      7
                    ],
                    'error': {
                      'mae': 5,
                      'smape': 6
                    }
                  }
                ],
                [
                  {
                    'data': [
                      2,
                      2,
                      2
                    ],
                    'error': {
                      'mae': 5,
                      'smape': 6
                    }
                  },
                  {
                    'data': [
                      3,
                      3,
                      3
                    ],
                    'error': {
                      'mae': 5,
                      'smape': 6
                    }
                  },
                  {
                    'data': [
                      4,
                      4,
                      4
                    ],
                    'error': {
                      'mae': 5,
                      'smape': 6
                    }
                  },
                  {
                    'data': [
                      5,
                      5,
                      5
                    ],
                    'error': {
                      'mae': 5,
                      'smape': 6
                    }
                  },
                  {
                    'data': [
                      6,
                      6,
                      6
                    ],
                    'error': {
                      'mae': 5,
                      'smape': 6
                    }
                  },
                  {
                    'data': [
                      7,
                      7,
                      7
                    ],
                    'error': {
                      'mae': 5,
                      'smape': 6
                    }
                  },
                  {
                    'data': [
                      7,
                      7,
                      7
                    ],
                    'error': {
                      'mae': 5,
                      'smape': 6
                    }
                  },
                  {
                    'data': [
                      7,
                      7,
                      7
                    ],
                    'error': {
                      'mae': 5,
                      'smape': 6
                    }
                  }
                ],
                [
                  {
                    'data': [
                      2,
                      2,
                      2
                    ],
                    'error': {
                      'mae': 5,
                      'smape': 6
                    }
                  },
                  {
                    'data': [
                      3,
                      3,
                      3
                    ],
                    'error': {
                      'mae': 5,
                      'smape': 6
                    }
                  },
                  {
                    'data': [
                      4,
                      4,
                      4
                    ],
                    'error': {
                      'mae': 5,
                      'smape': 6
                    }
                  },
                  {
                    'data': [
                      5,
                      5,
                      5
                    ],
                    'error': {
                      'mae': 5,
                      'smape': 6
                    }
                  },
                  {
                    'data': [
                      6,
                      6,
                      6
                    ],
                    'error': {
                      'mae': 5,
                      'smape': 6
                    }
                  },
                  {
                    'data': [
                      7,
                      7,
                      7
                    ],
                    'error': {
                      'mae': 5,
                      'smape': 6
                    }
                  },
                  {
                    'data': [
                      7,
                      7,
                      7
                    ],
                    'error': {
                      'mae': 5,
                      'smape': 6
                    }
                  },
                  {
                    'data': [
                      7,
                      7,
                      7
                    ],
                    'error': {
                      'mae': 5,
                      'smape': 6
                    }
                  }
                ]
              ]
            },
            "data": {
              "dataSetName": "Name of dataset",
              "graphs": [
                {
                  "label": "Graph A",
                  "data": [
                    {
                      "x": 2,
                      "y": 35
                    },
                    {
                      "x": 3,
                      "y": 38
                    },
                    {
                      "x": 4,
                      "y": 43
                    },
                    {
                      "x": 7,
                      "y": 83
                    },
                    {
                      "x": 8,
                      "y": 42
                    },
                    {
                      "x": 9,
                      "y": 15
                    },
                    {
                      "x": 9,
                      "y": 32
                    },
                    {
                      "x": 22,
                      "y": 55
                    }
                  ]
                },
                {
                  "label": "Graph B",
                  "data": [
                    {
                      "x": 2,
                      "y": 24
                    },
                    {
                      "x": 3,
                      "y": 15
                    },
                    {
                      "x": 4,
                      "y": 65
                    },
                    {
                      "x": 7,
                      "y": 78
                    },
                    {
                      "x": 8,
                      "y": 13
                    },
                    {
                      "x": 9,
                      "y": 12
                    },
                    {
                      "x": 9,
                      "y": 46
                    },
                    {
                      "x": 22,
                      "y": 69
                    }
                  ]
                },
                {
                  "label": "Graph C",
                  "data": [
                    {
                      "x": 2,
                      "y": 54
                    },
                    {
                      "x": 3,
                      "y": 55
                    },
                    {
                      "x": 4,
                      "y": 65
                    },
                    {
                      "x": 7,
                      "y": 14
                    },
                    {
                      "x": 8,
                      "y": 68
                    },
                    {
                      "x": 9,
                      "y": 72
                    },
                    {
                      "x": 9,
                      "y": 92
                    },
                    {
                      "x": 22,
                      "y": 44
                    }
                  ]
                }
              ]
            }
          }
        }

# The "/data" endpoint
class Data(Resource):
    def post(self):
        return "Hello from data"

# The "/storage/add" endpoint
class StorageAdd(Resource):
    def post(self, fileName, fileData):
        if not ValidateFileName(fileName):
            return "Invalid request!", 404
        else:
            WriteToPublic("storage", fileData, fileName)
            return "File added!"

# The "/storage/get" endpoint
class StorageGet(Resource):
    def get(self, fileName):
        if not ValidateFileName(fileName) or not ValidateFileExist("storage", fileName):
           return "Invalid request!", 404
        else:
            try:
                return send_file("public/storage/" + fileName, attachment_filename=fileName)
            except Exception as e:
                return str(e)

# The "/storage/get-all-names" endpoint
class StorageGetAllNames(Resource):
    def get(self):
        return GetFileNamesInFolder("storage")

# The "/combined" endpoint
class Combined(Resource):
    def post(self):
        return "Hello from combined"

# Endpoints
api.add_resource(Root, "/")
api.add_resource(Info, "/info")
api.add_resource(Fields, "/fields")
api.add_resource(Readme, "/readme")
api.add_resource(Render, "/render")
api.add_resource(Data, "/data")
api.add_resource(StorageAdd, "/storage/add/name=<string:fileName>&data=<string:fileData>")
api.add_resource(StorageGet, "/storage/get/name=<string:fileName>")
api.add_resource(StorageGetAllNames, "/storage/get-all-names")
api.add_resource(Combined, "/combined")

# Start connection
if __name__ == "__main__":
    app.run(debug=False, port="5000", host="0.0.0.0")
