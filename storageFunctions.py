import re
import glob
import json
import requests
import wget
from validationFunctions import ValidateRelativePath, ValidateFileName, ValidateFileExist

# Write a file to the public folder
def WriteToPublic(relativePath, fileData, fileName):
    if not ValidateRelativePath(relativePath) or not ValidateFileName(fileName):
        return "Did not upload file: Please ensure everything is valid"

    # Should relative path be used?
    if relativePath != "":
        saveLocation = "public/" + relativePath + "/" + fileName
    else:
        saveLocation = "public/" + fileName

    fileData.save(saveLocation)
    return "File has been uploaded"

# Get text from a file in the public folder
def GetTextFromPublic(relativePath, fileName):
    if not ValidateRelativePath(relativePath) or not ValidateFileName(fileName) or not ValidateFileExist(relativePath, fileName, "public/"):
        return "Invalid request!"

    # Should relative path be used?
    if relativePath != "":
        readFile = open("public/" + relativePath + "/" + fileName, "r")
    else:
        readFile = open("public/" + fileName, "r")

    data = readFile.read()
    return data

# Get JSON from a file in the public folder
def GetJsonFromPublic(relativePath, fileName):
    return GetJsonData(relativePath, fileName, "public/")

# Get JSON from a file in the private folder
def GetJsonFromPrivate(relativePath, fileName):
    return GetJsonData(relativePath, fileName, "private/")

# Get JSON from a file
def GetJsonData(relativePath, fileName, localFolder):
    if not ValidateRelativePath(relativePath) or not ValidateFileName(fileName) or not ValidateFileExist(relativePath, fileName, localFolder):
        return "Invalid request!"

    # Should relative path be used?
    if relativePath != "":
        readFile = open(localFolder + relativePath + "/" + fileName, "r")
    else:
        readFile = open(localFolder + fileName, "r")

    data = json.load(readFile)
    return data

# Get array of all files in folder
def GetFileNamesInFolder(relativePath):
    if not ValidateRelativePath(relativePath):
        return "Invalid request!"

    # Make array with all file names at path
    fileNameArr = glob.glob("public/" + relativePath + "/*")
    return fileNameArr

# Upload to Google Cloud Platform
def UploadToGCP(fileData, fileName):
    if not ValidateFileName(str(fileName)):
        return False
    urls = GetJsonFromPrivate("noGithub", "productionData.json")
    url = str(urls["uploadURL"]) + "?build_id=" + str(fileName)
    files = {'file': fileData}
    r = requests.post(url, files=files)
    return fileName

# Download from Google Cloud Platform
def DownloadFromGCP(fileName):
    if not ValidateFileName(fileName):
        return False
    urls = GetJsonFromPrivate("noGithub", "productionData.json")
    url = urls["downloadURL"] + str(fileName) + ".predict"
    wget.download(url, "private/data/" + str(fileName) + ".predict")
    return open("private/data/" + str(fileName) + ".predict", "r")

# Used for testing purposes
def MockUploadToGCP(fileData):
    noGithub = GetJsonFromPrivate("noGithub", "privateData.json")
    uploadID = requests.post(noGithub["uploadURL"])
    return re.sub('[^0-9a-zA-Z_\- ]', '', uploadID.text)

# Used for testing purposes
def MockDownloadFromGCP(fileID):
    return open("public/storage/first_1000.csv", "r")
