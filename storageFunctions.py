import re
import glob
import base64

# Ensure not able to access folders below static/ and valid chars
def ValidateRelativePath(relativePath):
    backPath = re.search("\.\.", relativePath)
    notAllowedChars = re.search("[^\w\.\/-]", relativePath)

    if backPath == None and notAllowedChars == None:
        return True
    else:
        return False 

# Validate proper filename chars
def ValidateFileName(filename):
    return ValidateRelativePath(filename) 
    # ...as we wish to validate the same things

# Validate proper filen exists
def ValidateFileExist(relativePath, filename):
    # Validate input
    if not ValidateRelativePath(relativePath) or not ValidateFileName(filename):
        return

    # Should relative path be used?
    if relativePath != "":
        for fileInPath in glob.glob("public/" + relativePath + "/" + filename):
            if fileInPath == "public/" + relativePath + "/" + filename:
                return True
            else:
                return False
    else:
        for fileInPath in glob.glob("public/" + filename):
            if fileInPath[0] == "public/" + filename:
                return True
            else:
                return False


# Write a file to the static folder
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

# Get a file form the static folder
def GetFromPublic(relativePath, filename):
    # Validate input
    if not ValidateRelativePath(relativePath) or not ValidateFileName(filename) or not ValidateFileExist(relativePath, filename):
        return "Invalid request!"

    # Should relative path be used?
    if relativePath != "":
        reader = open("public/"+relativePath+"/"+filename, "r")
    else:
        reader = open("public/"+filename, "r")

    # Get and return data
    data = reader.read()
    return data

# Get array of all files in folder
def GetFileNamesInFolder(relativePath):
    # Validate input
    if not ValidateRelativePath(relativePath):
        return "Invalid request!"

    # Make array with all file names at path
    fileNameArr = glob.glob("public/" + relativePath + "/*")
    return fileNameArr