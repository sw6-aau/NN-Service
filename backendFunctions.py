import requests
import re
import uuid
import json
from storageFunctions import UploadToGCP, DownloadFromGCP, GetJsonFromPublic, GetJsonFromPrivate, GetTextFromPublic
from validationFunctions import ValidateNumber, ValidateNumNotNegative, ValidateStringNoSymbol, IsEmptyString, ValidateParamFile
from converterFunctions import CsvToTimeSeries, TimeSeriesToChartJs, TimeSeriesToGenericTsGraph, TimeSeriesToCsv

noGithub = GetJsonFromPrivate("noGithub", "productionData.json")
errorChart = GetJsonFromPublic("api", "errorChart.json")
errorHTML = errorChart["content"]

# Return error response
def ReturnErrorResponse(reason):
    return {
        "chart_type": "composite-scroll",
        "content": [
            errorChart,
            {
                "chart_type": "text",
                "content": "<div style='color: white; text-align: center; background-color: #630a0f;'><p style='margin: 0; padding: 5px;'>Reason: <i>" + str(reason) + "</i></p><div>"
            },
            {
                "chart_type": "markdown",
                "content": GetTextFromPublic("api", "documentation.md")
            }
        ]
    }

# Handle the request to /render
def HandleRenderPost(args):
    # Input validation, and error response
    if not ValidationOfRenderArgs(args):
        return ReturnErrorResponse("Failed input validation")

    # Fill preset values if desired
    if not args["preset"] == "m":
        args = FillPresetValues(args, args["preset"])

    # If no build_id is entered then generate one
    if IsEmptyString(args["build_id"]):
        if args["preset"] == "p" and IsEmptyString(args["build_id"]):
            return ReturnErrorResponse("No build ID entered")
        args["build_id"] = re.sub("[^0-9a-zA-Z_\- ]", "", str(uuid.uuid4()))
    
    # If no datafile_id is entered then generate one
    if IsEmptyString(args["datafile_id"]):
        args["datafile_id"] = re.sub("[^0-9a-zA-Z_\- ]", "", str(uuid.uuid4()))

    # Upload files to GCP
    args = HandleUploadToCGP(args)
    if type(args) == str:
        return ReturnErrorResponse(args)

    # Save orginal file as in time series format
    originalFile = CsvToTimeSeries(DownloadFromGCP(args["datafile_id"]), "data set", False)

    # Train if desired by user
    if args["option"] == "tp" or args["option"] == "t":
        trainParams = MakeTrainParams(args)
        url = str(noGithub["trainURL"]) + str(ConvertArgsToParams(trainParams))
        trainReq = requests.get(url)
        trainID = re.sub("[^0-9a-zA-Z_\- ]", "", trainReq.text)

        if ValidateStringNoSymbol(trainID) or not str(trainID) == str(args["build_id"]):
            # If only train, then return ID
            if args["option"] == "t":
                return MakeBuildIDChart(args["build_id"], args["datafile_id"])
        else:
            return ReturnErrorResponse("Failed in training stage")

    # Predict if desired by user
    if args["option"] == "tp" or args["option"] == "p":
        if args["option"] == "p" and (IsEmptyString(args["build_id"]) or IsEmptyString(args["datafile_id"])):
            return ReturnErrorResponse("No build ID entered for prediction")
        predictParams = MakePredictParams(args)
        url = str(noGithub["predictURL"]) + str(ConvertArgsToParams(predictParams))
        predictReq = requests.get(url)
        predictID = re.sub("[^0-9a-zA-Z_\- ]", '', predictReq.text)
        if not ValidateStringNoSymbol(predictID):
            return ReturnErrorResponse("Failed in predict stage: Invalid predictID")
        if not str(predictID) == str(args["build_id"]):
            return ReturnErrorResponse("Failed in predict stage: Incorrect match of IDs '" + str(predictID) + "' != '" + str(args["build_id"]) + "'")

    # Download datafile from GCP
    if args["option"] == "v":
        if IsEmptyString(args["datafile_id"]):
            return ReturnErrorResponse("No data file ID entered for visualization")
        if args["file_settings"] == "prev":
            data = DownloadFromGCP(args["datafile_id"] + ".predict")
        else:
            data = DownloadFromGCP(args["datafile_id"])
    elif args["option"] == "print":
        if IsEmptyString(args["datafile_id"]):
            return ReturnErrorResponse("No data file ID entered for printing data ('Visualize Results' version)")
        data = DownloadFromGCP(args["datafile_id"])
    else:
        data = DownloadFromGCP(args["build_id"] + ".predict")

    # Make all the charts needed to display
    aSTEPDataOuptput = CsvToTimeSeries(data, "Data Set", True)
    inputSize = int(args["window_rnn"]) + int(args["horizon"]) - int(1) 
    print(inputSize)
    if (args["option"] == "v" and not args["file_settings"] == "prev") or args["option"] == "print":
        chartTimeSeries = TimeSeriesToGenericTsGraph(originalFile, aSTEPDataOuptput, inputSize, True)
    else:
        chartTimeSeries = TimeSeriesToGenericTsGraph(originalFile, aSTEPDataOuptput, inputSize, False)
    originalChartJs = TimeSeriesToChartJs(originalFile, "line", "Input")
    predictChartJs = TimeSeriesToChartJs(aSTEPDataOuptput, "line", "Predict")
    buildIDChart = MakeBuildIDChart(args["build_id"], args["datafile_id"])
    outputDataAstep = MakeDataChart("Output - RFC0016", str(json.dumps(aSTEPDataOuptput, indent=4)))
    outputDataCsv = MakeDataChart("Output - CSV", str(TimeSeriesToCsv(aSTEPDataOuptput)))
    inputDataAstep = MakeDataChart("Input - RFC0016", str(json.dumps(originalFile, indent=4)))
    inputDataCsv = MakeDataChart("Input - CSV", str(TimeSeriesToCsv(originalFile)))

    return {
        "chart_type": "composite-scroll",
        "content": [
            buildIDChart,
            {
                "chart_type": "composite",
                "content": [chartTimeSeries, originalChartJs, predictChartJs, outputDataAstep, outputDataCsv, inputDataAstep, inputDataCsv]
            }
        ]
    }

# Handles file uploads to GCP, based upon the many options
# Returns updated version of args
def HandleUploadToCGP(args):
    newArgs = args

    # Upon train and predict, and train
    if newArgs["option"] == "tp" or newArgs["option"] == "t":
        # Train data:
        newArgs = UploadBasedOnSettings(args["train_settings"], newArgs["data-input"], args, False)
        if type(newArgs) == str:
            return newArgs
        # Predict data:
        newArgs = UploadBasedOnSettings(args["file_settings"], newArgs["data-file"], args, True)
        return newArgs

    # Upon visualize or predict
    if newArgs["option"] == "v" or newArgs["option"] == "p":
        newArgs = UploadBasedOnSettings(args["file_settings"], newArgs["data-input"], args, True)
    
    return newArgs

# Upload a file based upon "prev", "csv", or "rfc" setting
def UploadBasedOnSettings(setting, fileToUpload, args, setDatafile):
    newArgs = args
    # If using a previously uploaded file
    if setting == "prev":
        if setDatafile:
            if IsEmptyString(newArgs["datafile_id"]):
                return "No file ID entered!"
            else:
                return newArgs # as datafile_id is already set
        else:
            if IsEmptyString(newArgs["build_id"]):
                return "No file ID entered!"
            else:
                return newArgs # as datafile_id is already set
    # If upload is of CSV type
    elif setting == "csv":
        if setDatafile:
            uploadID = UploadToGCP(fileToUpload, newArgs["datafile_id"])
            newArgs["datafile_id"] = uploadID
        else:
            uploadID = UploadToGCP(fileToUpload, newArgs["build_id"])
            newArgs["build_id"] = uploadID
    #If upload is of RFC0016 type
    elif setting == "rfc":
        tempID = re.sub("[^0-9a-zA-Z_\- ]", "", str(uuid.uuid4()))
        tempUploadID = UploadToGCP(fileToUpload.stream.read(), tempID)
        tempFile = DownloadFromGCP(tempID)
        data = TimeSeriesToCsv(json.loads(tempFile.read()))
        if setDatafile:
            uploadID = UploadToGCP(data, newArgs["datafile_id"])
            newArgs["datafile_id"] = uploadID
        else:
            uploadID = UploadToGCP(data, newArgs["build_id"])
            newArgs["build_id"] = uploadID
    # If none of the above
    else:
        return "Invalid file setting!"

    return newArgs

# Take out the params needed for /train
def MakeTrainParams(args):
    trainParams = {}
    trainParams["build_id"] = args["build_id"]
    trainParams["horizon"] = args["horizon"]
    trainParams["dropout"] = args["dropout"]
    trainParams["epoch"] = args["epoch"]
    trainParams["hid_cnn"] = args["hid_cnn"]
    trainParams["hid_rnn"] = args["hid_rnn"]
    trainParams["window_rnn"] = args["window_rnn"]
    trainParams["windows_hw"] = args["windows_hw"]
    trainParams["skip_rnn"] = args["skip_rnn"]
    return trainParams

# Take out the params needed for /predict
def MakePredictParams(args):
    predictParams = {}
    predictParams["build_id"] = args["build_id"]
    predictParams["datafile_id"] = args["datafile_id"]
    return predictParams

# Fill preset values
def FillPresetValues(args, presetName):
    preset = GetJsonFromPublic("data", "presetValues.json")
    presetArr = preset[presetName]
    args["horizon"] = presetArr[0]
    args["dropout"] = presetArr[1]
    args["hid_cnn"] = presetArr[2]
    args["hid_rnn"] = presetArr[3]
    args["window_rnn"] = presetArr[4]
    args["windows_hw"] = presetArr[5]
    args["skip_rnn"] = presetArr[6]
    return args

# Make a build ID HTML chart
def MakeBuildIDChart(buildID, datafileID):
    return {
        "chart_type": "text",
        "content": "<div style='color: white; text-align: center; background-color: #000000; padding: 2px'><p style='margin: 0; padding: 5px;'>Build ID: <i>" + str(buildID) + "</i></p><pstyle='margin: 0; padding: 5px;'>Data File ID: <i>" + str(datafileID) + "</i></p><div>"
    }

# Make a data chart to display raw data to users
def MakeDataChart(name, data):
    return {
        "chart_type": "text",
        "name": name,
        "content": "<div style='width: 95%; height: 70vh; margin: 2.5%'><textarea style='width: 100%; height: 100%; margin: 0'>" + data + "</textarea></div>"
    }

# Takes an array of args, and returns a HTML param string
def ConvertArgsToParams(args):
    first = True
    paramsString = "?"
    for arg in args:
        if not first:
            paramsString += "&"
        else:
            first = False
        paramsString += str(arg) + "=" + str(args[arg])
    return paramsString

# Validate input fields for /render are of correct format
def ValidationOfRenderArgs(args):
    checks = []
    checks.append(ValidateStringNoSymbol(args["option"]))

    if args["option"] == "tp" or args["option"] == "t":
        checks.append(ValidateStringNoSymbol(args["train_settings"]))
        checks.append(ValidateRenderNumber(args["epoch"]))
        checks.append(ValidateStringNoSymbol(args["preset"]))
        # Only check rest if manual-mode is chosen
        if ValidateStringNoSymbol(args["preset"]) and args["preset"] == "m":
            checks.append(ValidateRenderNumber(args["horizon"]))
            checks.append(ValidateRenderNumber(args["dropout"]))
            # Ensure dropout is <= 1
            if ValidateRenderNumber(args["dropout"]) and float(args["dropout"]) > 1:
                    print("ERROR: Argument '" + args["dropout"] +"' failed validation, as n > 1")
                    checks.append(False)
            checks.append(ValidateRenderNumber(args["hid_cnn"]))
            checks.append(ValidateRenderNumber(args["hid_rnn"]))
            checks.append(ValidateRenderNumber(args["window_rnn"]))
            checks.append(ValidateRenderNumber(args["windows_hw"]))
            checks.append(ValidateRenderNumber(args["skip_rnn"]))
    
    if args["option"] == "tp":
        checks.append(ValidateStringNoSymbol(args["file_settings"]))

    if args["option"] == "p":
        checks.append(ValidateStringNoSymbol(args["file_settings"]))
        checks.append(ValidateStringNoSymbol(args["datafile_id"]))
        checks.append(ValidateStringNoSymbol(args["build_id"]))

    if args["option"] == "v":
        checks.append(ValidateStringNoSymbol(args["file_settings"]))
        checks.append(ValidateStringNoSymbol(args["datafile_id"]))

    if args["option"] == "print":
        checks.append(ValidateStringNoSymbol(args["datafile_id"]))

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

# Handle request for data from /data
def HandleData(args):
    if IsEmptyString(args["datafile_id"]):
        return "No datafile ID entered to get data from! Please enter valid dataID 'Print Raw Data' option in 'What do you wish to do?'."
    elif not ValidateStringNoSymbol(args["datafile_id"]):
        return "Invalid datafile ID!"
    else:
        data = DownloadFromGCP(args["datafile_id"] + ".predict")
        return CsvToTimeSeries(data, "Data Set", True)
