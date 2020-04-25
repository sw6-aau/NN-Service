# Time-Series NN Forecasting: Documentation
*Group Sw602f20 "Time-Series NN Forecasting" service.*

## Mandatory fields:
*The following fields are mandatory to fill in values of:*

**Horizon:** How many time steps ahead the net should try to predict.

**Dropout:** How many percents of unit weights it should forget between each component layer. Helps prevent overfitting.

**RNN-skip number of time-steps skips:** How many time steps it should skip in the RNN-skip network. For a dataset where one input corresponds to a hour, 24 skip time-steps would mean that RNN-skip would train predicting time-steps where one time-step corresponds to one day.

**Param preset:** Choose parameter preset if you have chosen to train on a preset dataset. Here you can also chose "Manual-mode", where you can set the other parameters.

## Manual fields:
*If you have chosen "Manual-mode" in Param preset, then you can insert the parameters manually from your own hypertuning.*

**Epochs:** How many epochs the model should train in.

**Autoencoder CNN hidden units:** How many hidden units will be in the autoencoder convultional and deconvolutional layers.

**RNN hidden units:** How many hidden units will be in the the hidden state in the regular RNN component.

**RNN-skip hidden units:** How many hidden units will be in the the hidden state in the RNN-skip component.

**RNN Window size:** How big a window that should be predicted in the RNN. For example, if the window was 24 * 7, in a dataset where each time-step is one hour, the RNN would train predicting the next hour in 24 * 7 time-steps, see how right it were in these 24 * 7 predictions and adjusts its weight. This will repeat for the whole training dataset.  

**Highway window**: *? for now*

**Activation function output:** Which activation function should be used on the output.

**Activation function autoencoder:** Which activation function should be used on the autoencoder convolution and deconvolution laye