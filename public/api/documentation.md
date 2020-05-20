# Time-Series NN Forecasting: Documentation
*Group Sw602f20 "Time-Series NN Forecasting" service.*

## Option fields
*The following fields are options for what you wish to do:*

**Input data:** Here you can upload the dataset in either a comma-separated .csv file or aSTEP RFC0016 file format. Please note that currently the data you upload will be publicly availible to everyone using this service, if they know the ID.

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

**RNN Hidden Units:** How many hidden units will be in the the hidden state in the short and long term Gated Recurrent Units (GRU) the network uses for recurrent layers.

**Short-RNN Window Size:** How big a window that should be predicted by th. For example, if the window was 24 * 7, in a dataset where each time-step is one hour, the RNN would train predicting the next hour in 24 * 7 time-steps, see how right it were in these 24 * 7 predictions and adjusts its weight. This will repeat for the whole training dataset.  

**Long-RNN Window Size:** How many time steps it should skip in the RNN-skip network. For a dataset where one input corresponds to a hour, 24 skip time-steps would mean that RNN-skip would train predicting time-steps where one time-step corresponds to one day.

**Highway Window:** How many hidden units the highway window linear layer should use.

## Buttons:

**Visualise Results:** Press this to run the service with your applied settings. 

**Print Raw Results:** Get the output data in RFC0016 format, based upon the build ID
