import csv
from validationFunctions import ValidateInt, ValidateAstepTimeSeries
from storageFunctions import GetJsonFromPublic

# Convert from CSV to aSTEP-time-series format
def CsvToTimeSeries(csvFile, dataSetName):
    outputObj = {
        "dataSetName": dataSetName,
        "graphs": []
    }
    reader = csv.reader(csvFile, delimiter=",")
    columnIndex = 0
    line = 0
    first = True

    # Create the graph objects, and ignore first row
    for row in reader:
        if first == True:
            first = False
        else:
            if line == 0:
                for column in row:
                    outputObj["graphs"].append(MakeDefaultGraphObj("Graph " + str(columnIndex)))
                    columnIndex += 1

            columnIndex = 0
            for column in row:
                outputObj["graphs"][columnIndex]["data"].append(MakeDataPointObj(line, column))
                columnIndex += 1
            line += 1

    return outputObj


# Make a default graph object
def MakeDefaultGraphObj(label):
    defaultObj = {
        "label": label,
        "data": []
    }
    return defaultObj

# Make a data-point object
def MakeDataPointObj(x, y):
    dataObj = {
        "x": int(x),
        "y": float(y)
    }
    return dataObj

# ===============

# aSTEP-time-series format to CSV
def TimeSeriesToCsv(timeSeriesData):
    data = []

    # Make array representation of all Y-values
    for graph in timeSeriesData["graphs"]:
        graphData = []
        for dataPoint in graph["data"]:
            graphData.append(dataPoint["y"])
        data.append(graphData)

    # Write to file
    saveFile = open("private/data/tsTo.csv", "w+")
    for index in range(0, len(data[0])):
        row = ""
        for arrayID in range(0, len(data)):
            row += str(data[arrayID][index])
            if not arrayID == len(data) - 1:
                row += ","
        saveFile.write(row)
        if not index == len(data[0]) - 1:
            saveFile.write("\n")
    saveFile.close()

    readFile = open("private/data/tsTo.csv", "r")
    return readFile.read()

# ===============

# aSTEP-time-series format to chart.js graph
def TimeSeriesToChartJs(timeSeriesData, chartType, tabName):
    chartObj = {
        "chart_type": "time-series-data",
        "name": "Static: " + timeSeriesData["dataSetName"] + " (" + tabName + ")",
        "content": {
            "settings": {
                "to_chart": "chart-js",
                "chartJsType": chartType
            },
            "data": timeSeriesData
        }
    }
    return chartObj

# ===============

# aSTEP-time-series format to generic-time-series chart
# Note: Input of originalData and predict data should be TimeSeriesdata formatted
def TimeSeriesToGenericTsGraph(originalData, predictData, windowSize, cutPredict):
    # Input validation
    if not ValidateAstepTimeSeries(originalData) or not ValidateAstepTimeSeries(predictData):
        print("ERROR: Failed validation while converting to generic-time-series chart")
        return GetJsonFromPublic("api", "errorChart.json")

    chartObj = {
        "chart_type": "time-series-data",
        "name": "Prediction: " + originalData["dataSetName"],
        "content": {
            "settings": {
                "to_chart": "generic-time-series",
                "predictions": MakePredictionPart(predictData, cutPredict, windowSize),
                "inputSize": windowSize
            },
            "data": originalData
        }
    }
    return chartObj

# Make prediction-part of the generic-time-series chart
def MakePredictionPart(predictData, cutPredict, windowSize):
    predictionArr = []
    dataArr = []
    tempErrorDict = {
        "something": 0
    }
    predictSteps = int(len(predictData["graphs"][0]["data"]) / 20)

    # Go through all graphs and make a prediction array for them
    for graph in predictData["graphs"]:
        graphPredictions = []
        graphLenght = len(graph["data"])
        currentIndex = 0

        # Make prediction object for each x-value
        for dataPoint in graph["data"]:
            # If we want to "cut predict", then do not do anything the index before windowSize
            if cutPredict and currentIndex < windowSize:
                currentIndex += 1
                continue
            
            dataArr = []

            # How much in the future should be predicted for this index?
            if (currentIndex + predictSteps) >= graphLenght - 1:
                predictUntil = graphLenght - 1 - currentIndex
            else:
                predictUntil = predictSteps

            # Go through the predicted data and collect it
            for i in range(0, int(predictUntil)):
                dataArr.append(graph["data"][currentIndex + 1 + i]["y"])

            # Add to the prediction array
            graphPredictions.append(MakePredictionObj(dataArr, tempErrorDict))
            currentIndex += 1

        predictionArr.append(graphPredictions)

    return predictionArr

# Make individual prediction object
def MakePredictionObj(dataArr, errorDict):
    predictionObj = {
        "data": dataArr,
        "error": errorDict
    }
    return predictionObj
