# AWT PJ WS 21/22 Deep Encode 2

Repository for training and evaluation of different machine learning models to reduce the number of test encodes needed to identify the optimal encoding settings.

## About Deep Encode
![](docs/images/DeepEncode.png)
Video streaming content differs in terms of complexity and requires title-specific encoding settings to achieve a certain visual quality. Per-title encoding enables a more efficient and tailored video encoding ladder based on the complexity of a video. To take things a step further, per-scene encoding enables tailored video encoding ladders based on the complexity of each scene, rather than an entire video. However, conventional encoding solutions, such as per-title and per-scene, are computationally heavy and required a high amount of test encodes to identify the optimal encoding settings. The Deep Encode project utilizes machine learning models and provides encoding setting predictions in order to avoid the computationally heavy test encodes.

### Features
The scripts contained in this folder allow to:

1. Build a Gradient Boosting Decision Tree model and predict VMAF values using it.
2. Plot the data points(Bitrate/predcted VMAF) and calculate the convex hull in order to see how one resolution outperforms the other at a certain bitrate.
3. Build the encodding ladder and get the higher VMAF value at a certain bitrate using it.

### Development
The development is done using Python 3.9.7. The required moduls are matplotlib, numpy, pandans, scikit-learn, scipy.
## Set up
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
cd awt-pj-ws21-22-deepencode-2\src\GBDT
```




_A requirements file was generated that will allow the automatic installation of the modules with_

```
pip install -r requirements.txt
```

## Run
### Build and Train the model
The script model-new.py builds the GBDT model and predicts the VMAF values.

to run this script:
`python model-new.py` 
### Plot bitrate/VMAF pairs
The script plot_bitrate_vmaf.py plots the data points(bitrate, predicted VMAF) and calculates the convexhull for each video ID.

to run this script:
`python plot_bitrate_vmaf.py`
### Build encoding ladder
The script build_encoding_ladder.py builds the bitrate/VMAF ladders for each video ID.

to run this script:
`python build_encoding_ladder.py`

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
