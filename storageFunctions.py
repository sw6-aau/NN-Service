import re
import glob
import base64
import json

# Ensure not able to access folders below public/ and valid chars
def ValidateRelativePath(relativePath):
    # No need to check if nothing
    if relativePath == "":
        return True
    
    # Do regex to figure check
    backPath = re.search("\.\.", relativePath)
    notAllowedChars = re.search("[^\w\.\/-]", relativePath)

    # Decide what to do
    if backPath == None and notAllowedChars == None:
        return True
    else:
        return False 

# Validate proper filename chars
def ValidateFileName(filename):
    return ValidateRelativePath(filename) 
    # ...as we wish to validate the same things

# Validate file exists
def ValidateFileExist(relativePath, filename):
    # Validate input
    if not ValidateRelativePath(relativePath) or not ValidateFileName(filename):
        return False

    # Should relative path be used?
    if relativePath != "":
        for fileInPath in glob.glob("public/" + relativePath + "/" + filename):
            if fileInPath == "public/" + relativePath + "/" + filename:
                return True
            else:
                return False
    else:
        for fileInPath in glob.glob("public/" + filename):
            if fileInPath == "public/" + filename:
                return True
            else:
                return False


# Write a file to the public folder
# Note: Assumes input is base64 encoded
def WriteToPublic(relativePath, data, filename):
    # Validate input
    if not ValidateRelativePath(relativePath) or not ValidateFileName(filename):
        return

    # Should relative path be used?
    if relativePath != "":
        out = open("public/"+relativePath+"/"+filename, "w")
    else:
        out = open("public/"+filename, "w")

    # Write decoded data
    decodedBytes = base64.b64decode(data.encode('ascii'))
    decodedStr = str(decodedBytes, "utf-8")
    out.write(decodedStr)
    out.close

# Get text from a file in the public folder
def GetTextFromPublic(relativePath, filename):
    # Validate input
    if not ValidateRelativePath(relativePath) or not ValidateFileName(filename) or not ValidateFileExist(relativePath, filename):
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
    # Validate input
    if not ValidateRelativePath(relativePath) or not ValidateFileName(filename) or not ValidateFileExist(relativePath, filename):
        return "Invalid request!"

    # Should relative path be used?
    if relativePath != "":
        readFile = open("public/"+relativePath+"/"+filename, "r")
    else:
        readFile = open("public/"+filename, "r")

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