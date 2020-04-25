import re
import glob
import json
from validationFunctions import ValidateRelativePath, ValidateFileName, ValidateFileExist

# Write a file to the public folder
def WriteToPublic(relativePath, fileData, filename):
    # Validate input
    if not ValidateRelativePath(relativePath) or not ValidateFileName(filename):
        return "Did not upload file: Please ensure everything is valid"

    # Should relative path be used?
    if relativePath != "":
        saveLocation = "public/"+relativePath+"/"+filename
    else:
        saveLocation = "public/"+filename

    # Write data
    fileData.save(saveLocation)
    return "File has been uploaded"

# Get text from a file in the public folder
def GetTextFromPublic(relativePath, filename):
    # Validate input
    if not ValidateRelativePath(relativePath) or not ValidateFileName(filename) or not ValidateFileExist(relativePath, filename, "public/"):
        return "Invalid request!"

    # Should relative path be used?
    if relativePath != "":
        readFile = open("public/"+relativePath+"/"+filename, "r")
    else:
        readFile = open("public/"+filename, "r")

    # Get and return data
    data = readFile.read()
    return data

# Get text from a file in the public folder
def GetJsonFromPublic(relativePath, filename):
    return GetJsonData(relativePath, filename, "public/")

# Get text from a file in the public folder
def GetJsonFromPrivate(relativePath, filename):
    return GetJsonData(relativePath, filename, "private/")

# Get text from a file in the public folder
def GetJsonData(relativePath, filename, localFolder):
    # Validate input
    if not ValidateRelativePath(relativePath) or not ValidateFileName(filename) or not ValidateFileExist(relativePath, filename, localFolder):
        return "Invalid request!"

    # Should relative path be used?
    if relativePath != "":
        readFile = open(localFolder + relativePath+"/"+filename, "r")
    else:
        readFile = open(localFolder + filename, "r")

    # Get and return data
    data = json.load(readFile)
    return data

# Get array of all files in folder
def GetFileNamesInFolder(relativePath):
    # Validate input
    if not ValidateRelativePath(relativePath):
        return "Invalid request!"

    # Make array with all file names at path
    fileNameArr = glob.glob("public/" + relativePath + "/*")
    return fileNameArr