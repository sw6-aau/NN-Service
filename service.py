import werkzeug
from flask import Flask, send_file
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from storageFunctions import ValidateFileExist, ValidateFileName, WriteToPublic, GetTextFromPublic, GetJsonFromPublic, GetFileNamesInFolder
from backendFunctions import SendRenderDataToBackend

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
            "chart_type": "markdown",
            "content": GetTextFromPublic("api", "documentation.md")
        }

# The "/render" endpoint
class Render(Resource):
    def post(self):
        # Parse request and save to dictionary
        parser = reqparse.RequestParser()
        parser.add_argument("dataset", type=werkzeug.datastructures.FileStorage, location='files')
        parser.add_argument("hori")
        parser.add_argument("drout")
        parser.add_argument("skilentim")
        parser.add_argument("preset")
        parser.add_argument("epochs")
        parser.add_argument("authidCNN")
        parser.add_argument("hidRNN")
        parser.add_argument("hidRNNski")
        parser.add_argument("rnnwind")
        parser.add_argument("highwayWind")
        parser.add_argument("actitypout")
        parser.add_argument("actitypauto")
        args = parser.parse_args()
        
        renderData = SendRenderDataToBackend(args)
        
        return GetJsonFromPublic("api", "render.json")      

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
