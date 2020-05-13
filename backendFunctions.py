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
        if args["option"] == "tp" or args["option"] == "t":
            if not ValidateParamFile(args["data-input"]):
                return ReturnErrorResponse("No file has been uploaded, when it is expected")
            args["build_id"] = re.sub("[^0-9a-zA-Z_\- ]", "", str(uuid.uuid4()))
        elif args["option"] == "p":
            return ReturnErrorResponse("You need a build ID if you are predicting")

    # Upload file, if training is selected
    if args["option"] == "tp" or args["option"] == "t":
        uploadID = UploadToGCP(args["data-input"], args["build_id"])
        args["datafile_id"] = uploadID

    # Download orgiginal file if visualize or predict mode, or if using datafile
    if args["option"] == "p" or args["option"] == "v":
        if IsEmptyString(args["datafile_id"]):
            return ReturnErrorResponse("No datafile ID has been set")

    # Save orginal file as in time series format
    originalFile = CsvToTimeSeries(DownloadFromGCP(args["datafile_id"]), "data set")

    # Train if desired by user
    if args["option"] == "tp" or args["option"] == "t":
        trainParams = MakeTrainParams(args)
        url = str(noGithub["trainURL"]) + str(ConvertArgsToParams(trainParams))
        print(url)
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
        print(url)
        predictReq = requests.get(url)
        predictID = re.sub("[^0-9a-zA-Z_\- ]", '', predictReq.text)
        if not ValidateStringNoSymbol(predictID):
            return ReturnErrorResponse("Failed in predict stage: Invalid predictID")
        if not str(predictID) == str(args["build_id"]):
            return ReturnErrorResponse("Failed in predict stage: Incorrect match of IDs" + str(predictID) + " != " + str(args["build_id"]))

    # Download datafile from GCP
    if args["option"] == "v":
        if IsEmptyString(args["datafile_id"]):
            return ReturnErrorResponse("No data file ID entered for visualization")
        data = DownloadFromGCP(args["datafile_id"] + ".predict")
    else:
        data = DownloadFromGCP(args["build_id"] + ".predict")

    # Make all the charts needed to display
    aSTEPDataOuptput = CsvToTimeSeries(data, "Data Set")
    chartTimeSeries = TimeSeriesToGenericTsGraph(originalFile, aSTEPDataOuptput, 20, args["window_rnn"])
    originalChartJs = TimeSeriesToChartJs(originalFile, "line", "Input")
    predictChartJs = TimeSeriesToChartJs(aSTEPDataOuptput, "line", "Predict")
    buildIDChart = MakeBuildIDChart(args["build_id"], args["datafile_id"])
    outputDataAstep = MakeDataChart("Output - RFC0016", str(json.dumps(aSTEPDataOuptput, indent=4)))
    outputDataCsv = MakeDataChart("Output - CSV", str(TimeSeriesToCsv(aSTEPDataOuptput)))

    return {
        "chart_type": "composite-scroll",
        "content": [
            buildIDChart,
            {
                "chart_type": "composite",
                "content": [chartTimeSeries, originalChartJs, predictChartJs, outputDataAstep, outputDataCsv]
            }
        ]
    }

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

    if args["option"] == "p":
        checks.append(ValidateStringNoSymbol(args["datafile_id"]))
        checks.append(ValidateStringNoSymbol(args["build_id"]))

    if args["option"] == "v":
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
        return "No datafile ID entered to get data from! Please enter valid buildID or generate one via the 'Visualize Results' option. (TIP: Switch to 'Only visualize' mode)'"
    elif not ValidateStringNoSymbol(args["datafile_id"]):
        return "Invalid datafile ID!"
    else:
        data = DownloadFromGCP(args["datafile_id"] + ".predict")
        return CsvToTimeSeries(data, "Data Set")
