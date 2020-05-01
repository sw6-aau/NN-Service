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

    # First create the graph objects
    for row in reader:
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

# aSTEP-time-series format to chart.js graph
def TimeSeriesToChartJs(timeSeriesData, chartType):
    chartObj = {
        "chart_type": "time-series-data",
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
def TimeSeriesToGenericTsGraph(originalData, predictData, predictSteps):
    # Input validation
    if not ValidateInt(predictSteps) or not ValidateAstepTimeSeries(originalData) or not ValidateAstepTimeSeries(predictData):
        print("ERROR: Failed validation while converting to generic-time-series chart")
        return GetJsonFromPublic("api", "errorChart.json")
    
    chartObj = {
        "chart_type": "time-series-data",
        "content": {
            "settings": {
                "to_chart": "generic-time-series",
                "predictions": MakePredictionPart(predictData, predictSteps)
            },
            "data": originalData
        }
    }
    return chartObj

# Make prediction-part of the generic-time-series chart
def MakePredictionPart(predictData, predictSteps):
    predictionArr = []
    dataArr = []
    tempErrorDict = {
        "something": 0
    }

    # Go through all graphs and make a prediction array for them
    for graph in predictData["graphs"]:
        graphPredictions = []
        graphLenght = len(graph["data"])
        currentIndex = 0

        # Make prediction object for each x-value
        for dataPoint in graph["data"]:
            dataArr = []

            # How much in the future should be predicted for this index?
            if (currentIndex + predictSteps) >= graphLenght - 1:
                print(">")
                predictUntil = graphLenght - 1 - currentIndex
            else:
                print("<")
                predictUntil = predictSteps

            # Go through the predicted data and collect it
            for i in range(0, predictUntil):
                print("-")
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