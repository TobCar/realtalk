# RealTalk
Detects fake voices in YouTube videos with 94% accuracy and alerts the user to prevent misinformation.

## Team Members

Tobias Carryer - Did the machine learning stuff

Shannon Hogan - Made the Python server

John Lee - Also made the Python server

Kyle Meade - Made the Chrome extension

## Machine Learning Architecture

We use multiple 1D convolutional neural network layers followed by two fully connected layers and a third fully connected output layer. We implement the model architecture with Keras in [model_architecture.py](server/ml_model/model_architecture.py). Take a look at [pipeline.py](server/ml_model/pipeline.py) to see how we train the model. Our approach achieves 94% binary classification accuracy on the [ASVspoof 2019 real PA](https://www.asvspoof.org) dataset, making it excellent at detecting most synthesised voices.
