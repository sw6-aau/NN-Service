import werkzeug
from flask import Flask, send_file, request, Response
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from storageFunctions import GetTextFromPublic, GetJsonFromPublic
from backendFunctions import HandleRenderPost, HandleData

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
        return GetJsonFromPublic("api", "info.json")

# The "/fields" endpoint
class Fields(Resource):
    def get(self):
        return GetJsonFromPublic("api", "fields.json")

# The "/readme" endpoint
class Readme(Resource):
    def get(self):
        return {
            "chart_type": "composite-scroll",
            "content": [
                {
                    "chart_type": "text",
                    "content": "<div style='color: white; text-align: center; background-color: #cc7416; padding: 2px'><h1 style='position: relative; top: 20px;'>! IMPORTANT !</h1><p style='margin: 20px;'>Training and prediction will be done on a server, so it will take some time to get a result.</p></div>"
                },
                {
                    "chart_type": "markdown",
                    "content": GetTextFromPublic("api", "documentation.md")
                }
            ]
        }

# The "/render" endpoint
class Render(Resource):
    def post(self):
        # Parse request and save to dictionary
        parser = reqparse.RequestParser()
        parser.add_argument("train_settings")
        parser.add_argument("file_settings")
        parser.add_argument("data-file", type=werkzeug.datastructures.FileStorage, location='files')
        parser.add_argument("data-input", type=werkzeug.datastructures.FileStorage, location='files')
        parser.add_argument("option")
        parser.add_argument("datafile_id")
        parser.add_argument("build_id")
        parser.add_argument("horizon")
        parser.add_argument("dropout")
        parser.add_argument("preset")
        parser.add_argument("epoch")
        parser.add_argument("hid_cnn")
        parser.add_argument("hid_rnn")
        parser.add_argument("window_rnn")
        parser.add_argument("windows_hw")
        parser.add_argument("skip_rnn")
        args = parser.parse_args()
        renderHTML = HandleRenderPost(args)

        return renderHTML

# The "/data" endpoint
class Data(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("datafile_id")
        args = parser.parse_args()
        return HandleData(args)

# The "/combined" endpoint
class Combined(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("train_settings")
        parser.add_argument("file_settings")
        parser.add_argument("data-file", type=werkzeug.datastructures.FileStorage, location='files')
        parser.add_argument("data-input", type=werkzeug.datastructures.FileStorage, location='files')
        parser.add_argument("option")
        parser.add_argument("datafile_id")
        parser.add_argument("build_id")
        parser.add_argument("horizon")
        parser.add_argument("dropout")
        parser.add_argument("preset")
        parser.add_argument("epoch")
        parser.add_argument("hid_cnn")
        parser.add_argument("hid_rnn")
        parser.add_argument("window_rnn")
        parser.add_argument("windows_hw")
        parser.add_argument("skip_rnn")
        args = parser.parse_args()
        renderHTML = HandleRenderPost(args)

        return {
            "data": HandleData(args),
            "render": renderHTML
        }

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
    app.run(threaded=True, debug=False, port="5000", host="0.0.0.0")
