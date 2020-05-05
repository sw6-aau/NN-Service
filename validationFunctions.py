import re
import glob

# Validate that it is not an empty string
def IsEmptyString(str):
    if str == "":
        print("ERROR: Empty string found")
        return True
    else:
        return False

# Validate if it is a number (float) via regex
def ValidateNumber(num):
    if IsEmptyString(num):
        return False
    test = re.search("[^0-9.-]", str(num))
    if test == None:
        return True
    else:
        print("ERROR: '" + num + "' is NaN (float)")
        return False

# Validate if it is a number (int) via regex
def ValidateInt(num):
    if IsEmptyString(num):
        return False
    test = re.search("[^0-9-]", str(num))
    if test == None:
        return True
    else:
        print("ERROR: '" + num + "' is NaN (int)")
        return False

# Validate that a number (float) is not negative
def ValidateNumNotNegative(num):
    if IsEmptyString(num):
        return False
    n = float(num)
    if n < 0:
        print("ERROR: '" + num + "' is negative")
        return False
    else:
        return True

# Validate that text is only letters and numbers via regex
def ValidateStringNoSymbol(string):
    test = re.search("[^0-9a-zA-Z_\- ]", string)
    if test == None:
        return True
    else:
        print("ERROR: '" + string + "' is not a valid string")
        return False

# Ensure not able to access folders below intended folder and has valid chars
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
    # First validate the input params
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

# Validate JSON-object is of aSTEP-time-series format
def ValidateAstepTimeSeries(obj):
    if not type(obj) is dict:
        return False
    
    if not "dataSetName" in obj or not "graphs" in obj:
        return False
    else:
        return True