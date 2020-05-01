import csv

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
        "x": x,
        "y": y
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

