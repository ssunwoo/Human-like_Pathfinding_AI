# Human-like_Pathfinding_AI

This repository contains python code for data preprocessing and jupyter notebook for machine learning.

The dataset used is the [Geolife GPS Trajectories](https://www.microsoft.com/en-us/download/details.aspx?id=52367)

Model is trained with LSTM which is RNN. We create coordinate arrays from map and GPS dataset for source and target. They are treated as sequences for seq2seq model.

When user enter addresses of start position and destination, visualization module loads the model and creates a map to show predicted route.

Framework used is TensorFlow, Keras, OSMnx, Folium, etc.
