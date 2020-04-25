import re
import glob

# Validate if it is a number via regex
def ValidateNumber(num):
    test = re.search("[^0-9.-]", num)
    if test == None:
        return True
    else:
        print("ERROR: '" + num + "' is NaN")
        return False

# Validate that a number is not negative
def ValidateNumNotNegative(num):
    n = float(num)
    if n < 0:
        print("ERROR: '" + num + "' is negative")
        return False
    else:
        return True

# Validate that text is only letters and numbers via regex
def ValidateStringNoSymbol(string):
    test = re.search("[^0-9a-zA-Z ]", string)
    if test == None:
        return True
    else:
        print("ERROR: '" + string + "' is not a valid string")
        return False

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
def ValidateFileExist(relativePath, filename, localFolder):
    # Validate input
    if not ValidateRelativePath(relativePath) or not ValidateFileName(filename):
        return False

    # Should relative path be used?
    if relativePath != "":
        for fileInPath in glob.glob(localFolder + relativePath + "/" + filename):
            if fileInPath == localFolder + relativePath + "/" + filename:
                return True
            else:
                return False
    else:
        for fileInPath in glob.glob(localFolder + filename):
            if fileInPath == localFolder + filename:
                return True
            else:
                return False