import requests
import re
import uuid
from storageFunctions import MockUploadToGCP, MockDownloadFromGCP, GetJsonFromPublic, GetJsonFromPrivate
from validationFunctions import ValidateNumber, ValidateNumNotNegative, ValidateStringNoSymbol
from converterFunctions import CsvToTimeSeries, TimeSeriesToChartJs, TimeSeriesToGenericTsGraph

noGithub = GetJsonFromPrivate("noGithub", "privateData.json")
errorChart = GetJsonFromPublic("api", "errorChart.json")
errorHTML = errorChart["content"]

# Handle the intial request to /render
# This sends HTML back to give feedback and initiate long polling GET request
def HandleRenderPost(args, serviceURL):
    # Input validation, and error response
    if not ValidationOfRenderArgs(args):
        return {"chart_type": "text", "content": errorHTML}
    
    # Upload file, and replace dataset with id in args
    uploadID = MockUploadToGCP(args["dataset"]) 
    del args["dataset"]
    args["dataset_id"] = uploadID
    params = ConvertArgsToParams(args)

    # Return initial HTML
    img = noGithub["waitingImg"]
    return {
            "chart_type": "text",
            "content": "<div style='color: white; text-align: center; background-color: #010b13; padding: 2px'><h2 style='margin-top: 1rem'>Please wait for calculations to finish.</h2><p><i>This page will update when calculations are done. It might take some time.</i></p><img style='text-align: center; margin-bottom: 0.5rem' src='" + img + "' width='50' alt=''></div></div><div style='width: 100%'><embed style='width: 100%' src='" + serviceURL + params + "'></div>"
        }

# Handle the second request to /render
# Gets data from backend when done with calculations
# Note this is intended to use long polling (wait a long time to resond)
def HandleRenderGet(args):
    # Input validation, and error response
    if not ValidationOfRenderArgs(args):
        return errorChart
    
    # Train if desired by user
    if args["option"] == "tp" or args["option"] == "t":
        trainReq = requests.post(url= noGithub["trainURL"], params = args)
        trainID = re.sub("[^0-9a-zA-Z_\- ]", "", trainReq.text)
        if ValidateStringNoSymbol(trainID):
            args["train_id"] = trainID
            # If only train, then return ID
            if args["option"] == "t":
                return {
                    "chart_type": "text",
                    "content": "<h3 style='text-align: center;'>Train ID: " + trainID + "</h3>"
                }
        else:
            return errorChart

    # Predict if desired by user
    if args["option"] == "tp" or args["option"] == "p":
        predictReq = requests.post(url= noGithub["predictURL"], params = args)     
        predictID = re.sub("[^0-9a-zA-Z_\- ]", '', predictReq.text)
        if ValidateStringNoSymbol(predictID):
            args["predict_id"] = predictID
        else:
            return errorChart

    # Download datafile from GCP
    if args["option"] == "v":
        data = MockDownloadFromGCP(args["build_id"])
    else:
        data = MockDownloadFromGCP(args["predict_id"])

    # Convert into chart data and aSTEP-RFC0016 format
    aSTEPData = CsvToTimeSeries(data, "Data Set")
    chart = TimeSeriesToGenericTsGraph(aSTEPData, aSTEPData, 2)
    
    return chart

# Takes an array of args, and returns a HTML param string
def ConvertArgsToParams(args):
    first = True
    paramsString = "?"
    for arg in args:
        if not first:
            paramsString += "&"
        else:
            first = False
        paramsString += arg + "=" + args[arg]
    return paramsString

# Validate input fields for /render are of correct format
def ValidationOfRenderArgs(args):
    checks = []
    
    checks.append(ValidateStringNoSymbol(args["option"]))
    checks.append(ValidateStringNoSymbol(args["build_id"]))
    checks.append(ValidateRenderNumber(args["horizon"]))
    checks.append(ValidateRenderNumber(args["dropout"]))
    # Ensure dropout is <= 1
    if ValidateRenderNumber(args["dropout"]) and float(args["dropout"]) > 1:
            print("ERROR: Argument '" + args["dropout"] +"' failed validation, as n > 1")
            checks.append(False)
    checks.append(ValidateRenderNumber(args["skip_rnn"]))
    checks.append(ValidateStringNoSymbol(args["preset"]))

    # Only check rest if manual-mode is chosen
    if ValidateStringNoSymbol(args["preset"]) and args["preset"] == "m":
        checks.append(ValidateRenderNumber(args["epoch"]))
        checks.append(ValidateRenderNumber(args["hid_cnn"]))
        checks.append(ValidateRenderNumber(args["hid_rnn"]))
        checks.append(ValidateRenderNumber(args["hid_skip_rnn"]))
        checks.append(ValidateRenderNumber(args["window_rnn"]))
        checks.append(ValidateRenderNumber(args["windows_hw"]))
        checks.append(ValidateStringNoSymbol(args["af_output"]))
        checks.append(ValidateStringNoSymbol(args["af_ae"]))

    # Only check these if the file exist
    if "dataset_id" in args:
        checks.append(ValidateStringNoSymbol(args["dataset_id"]))

    # Check if any validation failed
    for check in checks:
        if not check:
            return False

    return True

# Validate a /render number-argument lives up to requirements for numbers
def ValidateRenderNumber(arg):
    if not ValidateNumber(arg) or not ValidateNumNotNegative(arg):
        print("ERROR: Argument '" + arg +"' failed number validation")
        return False
    else:
        return True