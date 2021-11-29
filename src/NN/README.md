# AWT PJ WS 21/22 Deep Encode 2

Repository for training and evaluation of different machine learning models to reduce the number of test encodes needed to identify the optimal encoding settings.

## About Deep Encode
![](docs/images/DeepEncode.png)
Video streaming content differs in terms of complexity and requires title-specific encoding settings to achieve a certain visual quality. Per-title encoding enables a more efficient and tailored video encoding ladder based on the complexity of a video. To take things a step further, per-scene encoding enables tailored video encoding ladders based on the complexity of each scene, rather than an entire video. However, conventional encoding solutions, such as per-title and per-scene, are computationally heavy and required a high amount of test encodes to identify the optimal encoding settings. The Deep Encode project utilizes machine learning models and provides encoding setting predictions in order to avoid the computationally heavy test encodes.

### Features

### Development

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


**virtualenv**

_install virtual env with_
```
pip install virtualenv
```

_create a directory to save virtual environments_
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


_clone the github repository_

```
git clone https://git.tu-berlin.de/juliop1996/awt-pj-ws21-22-deepencode-2.git
```

_enter repository_

```
cd awt-pj-ws21-22-deepencode-2\src\NN
```




_A requirements file was generated that will allow the automatic installation of the modules with_

```
pip install -r requirements.txt
```

## Run

### Important commands

_to run the script_

```
python neuralnetworkmodel.py
```

## Documentation

## Tests

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
