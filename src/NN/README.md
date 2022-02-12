# AWT PJ WS 21/22 Deep Encode 2

Repository for training and evaluation of different machine learning models to reduce the number of test encodes needed to identify the optimal encoding settings.

## About Deep Encode
![](docs/images/DeepEncode.png)
Video streaming content differs in terms of complexity and requires title-specific encoding settings to achieve a certain visual quality. Per-title encoding enables a more efficient and tailored video encoding ladder based on the complexity of a video. To take things a step further, per-scene encoding enables tailored video encoding ladders based on the complexity of each scene, rather than an entire video. However, conventional encoding solutions, such as per-title and per-scene, are computationally heavy and required a high amount of test encodes to identify the optimal encoding settings. The Deep Encode project utilizes machine learning models and provides encoding setting predictions in order to avoid the computationally heavy test encodes.

### Features

Currently, the Scripts contained in this folder allow to:

- Build a convolutional neural network model, test it, and predict values with it.
- Plot data into graphs and calculate the convex hull in order to see how one resolution outperforms the other at a certain bitrate.
- Build the encodding ladder following Netflix´s bitrate ranges, the best setting for every bitrate range.

Note:
The instructions are written for Linux, specifically Ubuntu 20.04.3 LTS

### Development
The scripts are currently under development. The development is done using *Python 3.9.9*. The rest of the requirements can be found in the [requirements file (requirements.txt)](requirements.txt).

## Set up

### Starting 🚀

_
These instructions will allow you to get a copy of the project running on your local machine for development and testing purposes_

Look at **Deployment** to know how to deploy this project.


### Requirements 📋

_**Git**_

```
sudo apt update
sudo apt install git
```

_**Python 3.9.9**_
```
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3
```

_**Install Pip**_
```
sudo apt install python3-pip
```


**virtualenv**

_install virtual env with_
```
pip install virtualenv
```

_create a directory to save virtual environments and enter it_
```
mkdir virtualenvs
cd virtualenvs
```

_Set the environment_
```
virtualenv env
```

_To activate use_
```
source env/bin/activate
```

_To deactivate it use_
```
source env/bin/deactivate
```

### Installation 🔧

_Follow these steps once done with the **Requirements**:_

_**NOTE: Keep your virtual environment activated for the installation.**



_clone the github repository without history_

```
git clone --depth 1 -b main https://git.tu-berlin.de/juliop1996/awt-pj-ws21-22-deepencode-2.git
```

_enter repository_

```
cd awt-pj-ws21-22-deepencode-2/src/NN
```




_A requirements file was generated that will allow the automatic installation of the modules with_

```
pip install -r requirements.txt
```

## Run and coding ⌨️

### Structure of the code

_The features are divided into three different scripts which follow this order by logic: 1st  **neuralnetworkmodel.py**, 2nd **plot_video_data.py** and 3rd **build_encodding_ladder.py**._
_The first script trains the model and produces the prediction used for the second script to plot the data while the third script builds the final encodding ladder for every video._
_A filesystem is created automatically by the scripts in order to organize the results of the scripts and have a log of what is been done._

#### plots
_In this folder lay all the plots in which for every video id a folder was created._
_The plot of the respective video has the same name as the id of the video and contains the generated data in terms of bitrate and vmaf at different resolutions._

#### encodding_ladders
_In this folder lay all the encodding ladders of every video in pdf format._
_This folder contains folders which have the same name as the video id it corresponds._

### Important commands

_to run the scripts_

This one might take a little bit longer to start.
```
python neuralnetworkmodel.py
```
```
python plot_video_data.py
```

```
python build_encodding_ladder.py
```



## Authors

Team of Deep Encode (2)

-Vinzenz Jakob Benedikt Franke\
-Julio Cesar Perez Duran\
-Ruihan Zhang

## Contact

The team is available by the following emails:

Vinzenz Jakob Benedikt Franke: vinzenz.franke@campus.tu-berlin.de\
Julio Cesar Perez Duran: julio.cesar.perez.duran@campus.tu-berlin.de\
Ruihan Zhang: ruihan.zhang@campus.tu-berlin.de
