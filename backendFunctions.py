import requests
import re
from storageFunctions import GetJsonFromPublic, GetJsonFromPrivate
from validationFunctions import ValidateNumber, ValidateNumNotNegative, ValidateStringNoSymbol

noGithub = GetJsonFromPrivate("noGithub", "privateData.json")
apiURL = "http://172.17.0.2:80" 

# Get data from input fields, and send them to bakcend 
# Then handle response and return
def SendRenderDataToBackend(args):
    # Input validation, and error response
    if not ValidationOfRenderArgs(args):
        img = noGithub["errorImg"]
        return {
            "chart_type": "text",
            "content": "<div style='color: red; text-align: center;'><h1 style='position: relative; top: 20px;'>ERROR</h1><p style='margin: 20px;'>Please make sure input is of correct format.</p><img src='" + img + "' width='500' alt=''></div>"
        }
    
    # TODO: Parse args into request
    # TODO: Handle retrieved data

    return GetJsonFromPublic("api", "render.json")

# Validate input fields for /render are of correct format
def ValidationOfRenderArgs(args):
    checks = []
    
    checks.append(ValidateStringNoSymbol(args["option"]))
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

