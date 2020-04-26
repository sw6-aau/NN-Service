import re
import glob
import json
from validationFunctions import ValidateRelativePath, ValidateFileName, ValidateFileExist

# Write a file to the public folder
def WriteToPublic(relativePath, fileData, filename):
    if not ValidateRelativePath(relativePath) or not ValidateFileName(filename):
        return "Did not upload file: Please ensure everything is valid"

    # Should relative path be used?
    if relativePath != "":
        saveLocation = "public/"+relativePath+"/"+filename
    else:
        saveLocation = "public/"+filename

    fileData.save(saveLocation)
    return "File has been uploaded"

# Get text from a file in the public folder
def GetTextFromPublic(relativePath, filename):
    if not ValidateRelativePath(relativePath) or not ValidateFileName(filename) or not ValidateFileExist(relativePath, filename, "public/"):
        return "Invalid request!"

    # Should relative path be used?
    if relativePath != "":
        readFile = open("public/"+relativePath+"/"+filename, "r")
    else:
        readFile = open("public/"+filename, "r")

    data = readFile.read()
    return data

# Get JSON from a file in the public folder
def GetJsonFromPublic(relativePath, filename):
    return GetJsonData(relativePath, filename, "public/")

# Get JSON from a file in the private folder
def GetJsonFromPrivate(relativePath, filename):
    return GetJsonData(relativePath, filename, "private/")

# Get JSON from a file
def GetJsonData(relativePath, filename, localFolder):
    if not ValidateRelativePath(relativePath) or not ValidateFileName(filename) or not ValidateFileExist(relativePath, filename, localFolder):
        return "Invalid request!"

    # Should relative path be used?
    if relativePath != "":
        readFile = open(localFolder + relativePath+"/"+filename, "r")
    else:
        readFile = open(localFolder + filename, "r")

    data = json.load(readFile)
    return data

# Get array of all files in folder
def GetFileNamesInFolder(relativePath):
    if not ValidateRelativePath(relativePath):
        return "Invalid request!"

    # Make array with all file names at path
    fileNameArr = glob.glob("public/" + relativePath + "/*")
    return fileNameArr