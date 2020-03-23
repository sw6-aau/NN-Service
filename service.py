from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS

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
            "content": open("static/documentation.md", "r").read()
        }

# The "/render" endpoint
class Render(Resource):
    def post(self):
        return {
            'chart_type': 'chart-js',
            'content': {
                'data': [
                    {
                        'data': [
                            4,
                            9,
                            2
                        ],
                        'label': 'A'
                    },
                    {
                        'data': [
                            2,
                            3,
                            9
                        ],
                        'label': 'B'
                    }
                ],
                'labels': [
                    '1',
                    '2',
                    '3'
                ],
                'colors': [
                    {
                        'backgroundColor': 'rgba(148,159,177,0.2)',
                        'borderColor': 'rgba(148,159,177,1)',
                        'pointBackgroundColor': 'rgba(148,159,177,1)',
                        'pointBorderColor': '#fff',
                        'pointHoverBackgroundColor': '#fff',
                        'pointHoverBorderColor': 'rgba(148,159,177,0.8)'
                    },
                    {
                        'backgroundColor': 'rgba(77,83,96,0.2)',
                        'borderColor': 'rgba(77,83,96,1)',
                        'pointBackgroundColor': 'rgba(77,83,96,1)',
                        'pointBorderColor': '#fff',
                        'pointHoverBackgroundColor': '#fff',
                        'pointHoverBorderColor': 'rgba(77,83,96,1)'
                    }
                ],
                'type': 'line'
            }
        }

# The "/data" endpoint
class Data(Resource):
    def post(self):
        return "Hello from data"

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
api.add_resource(Combined, "/combined")

# Start connection
if __name__ == "__main__":
    app.run(debug=False, port="5000", host="0.0.0.0")