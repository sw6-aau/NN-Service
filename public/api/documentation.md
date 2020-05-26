# Time-Series NN Forecasting: Documentation
*Group Sw602f20 "Time-Series NN Forecasting" service.*

## Option fields
*The following fields are options for what you wish to do:*

**Input data:** Here you can upload the dataset in either a comma-separated .csv file or aSTEP RFC0016 file format. Please note that currently the data you upload will be publicly availible to everyone using this service, if they know the ID.
Example data-sets can be found here: https://github.com/sw6-aau/multvariant-time-series-datasets

**What do you wish to do?:** Here you can chose what should happen.

**Data File ID:** If you wish to do a datafile ID from a previous run. Leave this empty to use the file you upload.

**Build ID:** If you wish to do a build ID from a previous run. Note: This field is mandatory if you want to "Print Raw Results".

## Mandatory fields:
*The following fields are mandatory to fill in values of:*

**Epochs:** How many epochs the model should train in.

**Param Preset:** Choose parameter preset if you have chosen to train on a preset dataset. Here you can also chose "Manual-mode", where you can set the other parameters.

## Manual fields:
*If you have chosen "Manual-mode" in Param preset, then you can insert the parameters manually from your own hypertuning.*

**Horizon:** How many time steps ahead the model should try to predict.

**Dropout:** How many percents of unit weights it should forget between the convolutional layer, the short and long term recurrent layers. Dropout helps to prevent overfitting. *Note: Must have value 0 >= x <= 1*

**CNN Hidden Units:** How many hidden units will be in the convultional layer.

**Recurrent Layer Hidden Units:** How many hidden units will be in the the hidden state in the short term Gated Recurrent Units (GRU) the network uses.

**Recurrent Layer Window Size:** How big a window that should be predicted by the standard recurrent layer. For example, if the window was 24 * 7, in a dataset where each time-step is one hour, the RNN would train predicting the next hour in 24 * 7 time-steps, see how right it were in these 24 * 7 predictions and adjusts its weight.

**Recurrent-skip window size:** How many time steps it should skip in the RNN-skip network. For a dataset where one input corresponds to a hour, a skip window size of 24 and recurrent layer window size of 168 (24*7) time-steps would mean that the network will update the prediction weights of each day in the week only with input received on the same days. Mondays will consider timestamps from mondays, Tuesdays will consider timestamps from Tuesdays and so on.

**Highway Window:** How many hidden units the highway window linear layer should use.

## Buttons:

**Visualise Results:** Press this to run the service with your applied settings. 

**Print Raw Results:** Get the output data in RFC0016 format, based upon the build ID
