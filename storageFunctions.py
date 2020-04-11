import re
import glob

# Ensure not able to access folders below static/ and valid chars
def ValidateRelativePath(relativePath):
    backPath = re.search("\.\.", relativePath)
    allowedChars = re.search("[^\w\.\/]", relativePath)
    if backPath == None and allowedChars == None:
        return True
    else:
        return False 

# Write a file to the static folder
def WriteToPublic(relativePath, data, filename):
    # Validate input
    if not ValidateRelativePath(relativePath):
        return
    # Should relative path be used?
    if relativePath != "":
        out = open("public/"+relativePath+"/"+filename, "w")
    else:
        out = open("public/"+filename, "w")
    # Write data
    out.write(data)
    out.close

# Get a file form the static folder
def GetFromPublic(relativePath, filename):
    # Validate input
    if not ValidateRelativePath(relativePath):
        return "Invalid path!"
    # Should relative path be used?
    if relativePath != "":
        reader = open("public/"+relativePath+"/"+filename, "r")
    else:
        reader = open("public/"+filename, "r")
    # Get and return data
    data = reader.read()
    return data

# Get array of all files in folder
def GetFilesInFolder(relativePath):
    # Validate input
    if not ValidateRelativePath(relativePath):
        return "Invalid path!"
    # Make array with all file names at path
    fileNameArr = glob.glob("public/" + relativePath + "/*")
    return fileNameArr

    