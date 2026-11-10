# util

## qrcode.py

### def detect_roi( img, size_ratio = (2.5, 2.5), gap_ratio=0.25, th_area=20*20 ) -> (code, rect), (roi, roi_rect)

- **img**: numpy array dtype=uint8

	Input image data

- **size_ratio** (2.5, 2.5): (**width_ratio**, **height_ratio**) float

	(width, height) of roi is calculated as (width_QRcode * **width_ratio**, height_QRcode * **height_ratio**).

- **gap_ratio** 0.25: float

	The bottom of the ROI is top_QRcode - height_QRcode * **gap_ratio**.

- **th_area** 20*20: float

	Return QR code whose area is grater than **th_area**.

- **code**: unicode string

	It includes code of detected barcode.
	If a barcode is not detected, the *code* is *None*.

- **rect**: Rect

	It includes the position of detected barcode.
	If a barcode is not detected, the *Rect* is *None*.

	The *Rect* includes the attribute of *left*, *top*, *width*, and *height*

- **roi**: numpy array dtype=uint8

	It includes extracted ROI.

- **roi_rect**: Rect

	It includes the position of the ROI.

	The *Rect* includes the attribute of *left*, *top*, *width*, and *height*

## timer.py

It was deleted. Please use [WDT](https://github.com/mastnk/WDT) instead of timer.py.
	
## webcam.py

### class webcam
It is a simple class to obtain the image of webcam.

```
from util.webcam import webcam

cam = webcam()
img = cam.get_img()
```

*img* (numpy array uint8) includes an image captured by the webcam.

img[height, width, BGR].

- def **__init__**( self, device=0 )

	**device**: device ID

- def **get_img**( self ) -> img (numpy array uint8, [height, width, BGR])

	**img** is the captured image.

### class img_from_dir
It is a simple class which can provide the image randamply sampled from the directory.
It may be used instead of the **webcam** when you don't have the webcam.

```
from util.webcam import img_from_dir

cam = img_from_dir( 'imgs/' )
img = cam.get_img()
```

- def **__init__**( self, dir )

	**dir** should inlude only image file which cv2 can read.

- def **get_img**( self ) -> img (numpy array uint8, [height, width, BGR])

	**img** is the image randomly sampled from dir.


## cnn.py

cnn.py was deltede. Please use img2feat instead of cnn.py.

Install img2feat
```
% pip install img2feta
```

```
from img2feat import CNN
```

For more information of img2feat, please visit [https://github.com/mastnk/img2feat](https://github.com/mastnk/img2feat).

## regression.py

It is a simple wrapper for linear regression of [scikit-learn](https://scikit-learn.org/).

[Linear Models](https://scikit-learn.org/stable/modules/classes.html#module-sklearn.linear_model)

### def **fit_LinearRegression**( X, Y, W=None ) -> model

Fit and return [LinearRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html).

LinearRegression internally calls [scipy.linalg.lstsq](https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.lstsq.html) which relies on 
[the LAPACK routine dgelsd](http://www.netlib.org/lapack/explore-3.1.1-html/dgelsd.f.html).
It calculate the minimum norm solution for underdetermined systems.

[reference](https://stats.stackexchange.com/questions/240573/how-does-numpy-solve-least-squares-for-underdetermined-systems)


### def **fit_RidgeRegression**( X, Y, W=None, alpha = 0 ) -> model

Fit and return [Ridge](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html).

### def **fit_LogisticRegression**( X, Y, W=None, C=1 ) -> model

Fit and return [LogisticRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html).

### def **predict**( model, X ) -> pred (numpy array float32, [N,] )

**N** is the number of data, or X.shape[0].

If the model is the regressor, return the predict results.

If the model is the binary classifier, return the second class probability.

### def **ensemble_mean**( models, X ) -> -> pred (numpy array float32, [N,] )

**N** is the number of data, or X.shape[0].

**models** is a list of models.

It calculates an ensemble mean of prediction by models.

[sklearn.ensemble: Ensemble Methods](https://scikit-learn.org/stable/modules/classes.html#module-sklearn.ensemble)

### def save_model( filename, model )

Save the model with pickle.

### load_model( filename ) -> model

Load the model with pickle.

### def rmse( Ytrue, Ypred ) -> float

Calculate the rmse between Ytrue and Ypred.

### def accuracy( Ytrue, Ypred ) -> float

Calculate the accuracy between Ytrue and Ypred, where Ytrue should be {0,1}.

## server.py

The server function using [zmq](https://zeromq.org/languages/python/).

### def **ip**() -> string

Rturn ip address of the computer.

### def **server_start**( port=5556, func=None, verbose=False, imshow=False, imfile=None ):

Start the server which classifies the image.

- **func**

	The functor or the function whose argument is the image returns the analysis results in the dictionary.

- **port**: int

	The port for the communication.

- **verbose**: {True, False}

	If it is true, the server prints the analysis results.

- **imshow**: {True, False}

	If it is true, the server shows the analized image.

- **imfile**: string

	If it is specified, the server saves the analized image.

## client.py

### class Client

The client class using [zmq](https://zeromq.org/languages/python/).

```
from util.client import Client
c = Client( host='192.168.0.100', port=5556 )
data = c.send_img( img )
print( data )
```

- def **__init__**( self, host = 'localhost', port = 5556, timeout=1000 ):

	**host**: IP address of the server host

	**port**: port for the communication

	**timeout**: timeout in millisecond

- def **send_img**( self, img ) -> data (dict)

	**img** is the image in numpy array (uint8).
	
	The data is the analyzied results in the dictionary.
	If the error is occurred, data would be *None*.

---
2021/01/18 mtanaka@sc.e.titech.ac.jp


