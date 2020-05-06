import requests
import re
import uuid
from storageFunctions import UploadToGCP, MockDownloadFromGCP, GetJsonFromPublic, GetJsonFromPrivate, GetTextFromPublic
from validationFunctions import ValidateNumber, ValidateNumNotNegative, ValidateStringNoSymbol, IsEmptyString, ValidateParamFile
from converterFunctions import CsvToTimeSeries, TimeSeriesToChartJs, TimeSeriesToGenericTsGraph

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
        if args["option"] == "tp" or args["option"] == "t":
            if not ValidateParamFile(args["data-input"]):
                return ReturnErrorResponse("No file has been uploaded, when it is expected")
            args["build_id"] = re.sub("[^0-9a-zA-Z_\- ]", "", str(uuid.uuid4()))
        else:
            return ReturnErrorResponse("There should not be any buildID, when training")

    # Upload file, if no datafile_id has been set
    if IsEmptyString(args["datafile_id"]):
        uploadID = UploadToGCP(args["data-input"], args["build_id"])
        args["datafile_id"] = uploadID
    # Save original file in variable and reove from args
    originalFile = CsvToTimeSeries(args["data-input"], "data set")
    del args["data-input"]

    # Train if desired by user
    if args["option"] == "tp" or args["option"] == "t":
        trainParams = MakeTrainParams(args)
        url = str(noGithub["trainURL"]) + str(ConvertArgsToParams(trainParams))
        trainReq = requests.post(url)
        trainID = re.sub("[^0-9a-zA-Z_\- ]", "", trainReq.text)
        
        if ValidateStringNoSymbol(trainID) or not str(trainID) == str(args["build_id"]):
            # If only train, then return ID
            if args["option"] == "t":
                return MakeBuildIDChart(args["build_id"], args["datafile_id"])
        else:
            return ReturnErrorResponse("Failed in training stage")

    # Predict if desired by user
    if args["option"] == "tp" or args["option"] == "p":
        if args["option"] == "p" and IsEmptyString(args["build_id"]):
            return ReturnErrorResponse("No build ID entered for prediction")
        
        predictParams = MakePredictParams(args)
        url = str(noGithub["predictURL"]) + str(ConvertArgsToParams(predictParams))
        predictReq = requests.post(url)
        predictID = re.sub("[^0-9a-zA-Z_\- ]", '', predictReq.text)

        if not ValidateStringNoSymbol(predictID) or str(predictID) == str(args["build_id"]):
            return ReturnErrorResponse("Failed in predict stage")

    # Download datafile from GCP
    if args["option"] == "v":
        if IsEmptyString(args["datafile_id"]):
            return ReturnErrorResponse("No data file ID entered for visualization")
        data = MockDownloadFromGCP(args["datafile_id"])
    else:
        data = MockDownloadFromGCP(args["build_id"])

    # Make all the charts needed to display
    aSTEPDataOuptput = CsvToTimeSeries(data, "Data Set")
    chartTimeSeries = TimeSeriesToGenericTsGraph(originalFile, aSTEPDataOuptput, 20)
    chartJs = TimeSeriesToChartJs(aSTEPDataOuptput, "line")
    buildIDChart = MakeBuildIDChart(args["build_id"], args["datafile_id"])

    return {
        "chart_type": "composite-scroll",
        "content": [
            buildIDChart,
            {
                "chart_type": "composite",
                "content": [chartTimeSeries, chartJs]
            }
        ]
    }

# Take out the params needed for /train
def MakeTrainParams(args):
    trainParams = {}
    trainParams["build_id"] = args["build_id"]
    trainParams["horizon"] = args["horizon"]
    trainParams["dropout"] = args["dropout"]
    trainParams["skip_rnn"] = args["skip_rnn"]
    trainParams["epoch"] = args["epoch"]
    trainParams["hid_cnn"] = args["hid_cnn"]
    trainParams["hid_rnn"] = args["hid_rnn"]
    trainParams["window_rnn"] = args["window_rnn"]
    trainParams["windows_hw"] = args["windows_hw"]
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
    args["epoch"] = presetArr[0]
    args["hid_cnn"] = presetArr[1]
    args["hid_rnn"] = presetArr[2]
    args["hid_skip_rnn"] = presetArr[3]
    args["window_rnn"] = presetArr[4]
    args["windows_hw"] = presetArr[5]
    args["af_output"] = presetArr[6]
    args["af_ae"] = presetArr[7]
    return args

# Make a build ID HTML chart
def MakeBuildIDChart(buildID, datafileID):
    return {
        "chart_type": "text",
        "content": "<div style='color: white; text-align: center; background-color: #000000; padding: 2px'><p style='margin: 0; padding: 5px;'>Build ID: <i>" + str(buildID) + "</i></p><pstyle='margin: 0; padding: 5px;'>Data File ID: <i>" + str(datafileID) + "</i></p><div>" 
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
    checks.append(ValidateStringNoSymbol(args["datafile_id"]))
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
    if IsEmptyString(args["build_id"]):
        return "No build ID entered to get data from! Please enter valid buildID or generate one via the 'Visualize Results' option."
    elif not ValidateStringNoSymbol(args["build_id"]):
        return "Invalid Build ID!"
    else:
        data = MockDownloadFromGCP(args["build_id"])
        return CsvToTimeSeries(data, "Data Set")
