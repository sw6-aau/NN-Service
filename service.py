from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from storageFunctions import WriteToPublic, GetFromPublic, GetFilesInFolder

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
            "user_fields": [{
                "name": "input-graphs",
                "label": "Graphs",
                "default": "",
                "placeholder": "As JSON stiring",
                "type": "input"
            }],
            "developer_fields": [{
                "name": "input-graphs",
                "label": "Graphs",
                "default": "",
                "placeholder": "As JSON stiring",
                "type": "input"
            }]
        }

# The "/readme" endpoint
class Readme(Resource):
    def get(self):
        return {
            "chart_type": "markdown",
            "content": GetFromPublic("", "documentation.md")
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

# The "/storage" endpoint
class Storage(Resource):
    def post(self):
        WriteToPublic("storage","Hello mom", "something.txt")
        return "Hello from storage!"

    def get(self):
        returnFile = GetFromPublic("storage", "something.txt")
        return GetFilesInFolder("storage")

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
api.add_resource(Storage, "/storage")
api.add_resource(Combined, "/combined")

# Start connection
if __name__ == "__main__":
    app.run(debug=False, port="5000", host="0.0.0.0")
