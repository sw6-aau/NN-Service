import requests
from storageFunctions import GetJsonFromPublic

apiURL = "http://172.17.0.2:80" 

def SendRenderDataToBackend(args):
    
    # TODO: Input validation
    
    # Fill params (manual or from preset)
    if args["preset"] != "m":
        # Get data from the preset values
        presetValues = GetJsonFromPublic("data", "presetValues.json")
        presetData = presetValues[args["preset"]]
        arguments = {
            "dataset": args["dataset"],
            "hori": args["hori"],
            "drout": args["drout"],
            "skilentim": args["skilentim"],
            "epochs": presetData[0],
            "authidCNN": presetData[1],
            "hidRNN": presetData[2],
            "hidRNNski": presetData[3],
            "rnnwind": presetData[4],
            "highwayWind": presetData[5],
            "actitypout": presetData[6],
            "actitypauto": presetData[7]
        }
    else:
        arguments = {
            "dataset": args["dataset"],
            "hori": args["hori"],
            "drout": args["drout"],
            "skilentim": args["skilentim"],
            "epochs": args["epochs"],
            "authidCNN": args["authidCNN"],
            "hidRNN": args["hidRNN"],
            "hidRNNski": args["hidRNNski"],
            "rnnwind": args["rnnwind"],
            "highwayWind": args["highwayWind"],
            "actitypout": args["actitypout"],
            "actitypauto": args["actitypauto"]
        }
    

    trainedData = requests.get(url=apiURL, params=arguments)
    
    # TODO: Handle trained data

    return "TrainedData_InCorrectFormatForRender"