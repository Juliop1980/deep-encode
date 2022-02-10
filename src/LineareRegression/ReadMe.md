> # AWT PJ WS 21/22 Deep Encode 2

Repository for training and evaluation of different machine learning models to reduce the number of test encodes needed to identify the optimal encoding settings.

## About Deep Encode
![](docs/images/DeepEncode.png)
Video streaming content differs in terms of complexity and requires title-specific encoding settings to achieve a certain visual quality. Per-title encoding enables a more efficient and tailored video encoding ladder based on the complexity of a video. To take things a step further, per-scene encoding enables tailored video encoding ladders based on the complexity of each scene, rather than an entire video. However, conventional encoding solutions, such as per-title and per-scene, are computationally heavy and required a high amount of test encodes to identify the optimal encoding settings. The Deep Encode project utilizes machine learning models and provides encoding setting predictions in order to avoid the computationally heavy test encodes.

### Features
The scripts contained in this folder allow to:

1. Build a Lineare Regression model and predict VMAF values using it.
2. Plot the data points(Bitrate/predcted VMAF) and calculate the convex hull in order to see how one resolution outperforms the other at a certain bitrate.
3. Build the encodding ladder and get the higher VMAF value at a certain bitrate using it.

### Development
The development is done using R 4.1.0. The required moduls are dummies, ggplot2, metrics, ggally, dplyr,tidyr,forecast, ggmap, datetime, fpc.
## Set up
### Requirements 📋

_**R 4.1.2**_
```
download and install R  4.1.2
https://cran.r-project.org/bin/windows/base/

download and install R Studio
https://www.rstudio.com/products/rstudio/download/ 
(free version is enough)

```

_**download directory**_
```
Download Folder 
https://git.tu-berlin.de/juliop1996/awt-pj-ws21-22-deepencode-2/-/tree/main/data

Open DataInR.rmd with R Studio

```

## Run
### Build and Train the model
The script dataInR.rmd builds the Linear Regression model and predicts the VMAF values.

Run All 

### Plot bitrate/VMAF pairs/encodding Ladder
The dataFrame encoddingLadderFinished contains the final EncodingLadder (videoID, bitrate, resolution, maxVMAF)

### Convex hull ###

The ConvexHull Graphs are saved as .png in the Folder.  


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
