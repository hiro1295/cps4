# Cyber Physical Solution

**DON'T push to main**

## Installation

```
% pip install img2feat
% pip install WDT
```

[img2feat](https://github.com/mastnk/img2feat)

[WDT](https://github.com/mastnk/WDT)

## Getting started

### Line Trace
If you run on the robot, please run:

```
% python linetrace.py
```
or
```
% python sm_linetrace.py
```

If you run on the emulator without the robot, please run:
```
% python linetrace.py -e
```
or
```
% python sm_linetrace.py -e
```

*linetrace.py*: Line trace example without a state machine.

*sm_linetrace.py*: Line trace example with a state machine.

The emulator is in *raspythoncar/em_lib2wd.py*

### Recgnition

*ant-vs-bee/imgs_code/train* includes training images with the qr code.

*ant-vs-bee/imgs_code/test* includes test images with the qr code.

Model training:

```
% python train_model.py
```

*model_resnet18.pkl* is the trained model.

Sever starting:
```
% python server_classifier.py --port 5555
```

Client starting:
```
% python client_classifier.py --host [the server ip] --port 5555 --file_dir ant-vs-bee/imgs_code/test
```


## util/

APIs for Cyber Physical Solution. For the details, please check util/README.md .

### util.barcode39

APIs related to barcode. *detect_roi* detects the ROI from the image data based on the location of barcode.

### util.regression

APIs related to the regression. *fit_LinearRegression* builds the model with the pair of data (X,Y).

### util.cnn

It was deleted. Please use [img2feat](https://github.com/mastnk/img2feat).

### util.server

APIs related to the server.

### util.client

APIs related to the client.

### util.web_cam

APIs related to the web camera.

## dog-vs-cat/

## train.py

It is a sample code which builds the regression model to predict dog (0) or cat (1) from the featured converted by the cnn.

## server_classifier.py

It is a sample code which classifs the image to dog (0) or cat (1).

```% python server_classifier.py 5555```


## client_webcam.py

It is a sample code and class for the client.
*Client_webcam* can obtain the image from the web camera, throught the image data to the server, then receive the extracted information.

To use *Client_webcam*, the server should be realdy to response.

The IP of the server and the port are provided by the server program.

