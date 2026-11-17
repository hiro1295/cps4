import os
import glob
import numpy as np
import cv2
import concurrent.futures
import argparse

from img2feat import CNN
from util.qrcode import detect_roi
from util.regression import save_model, accuracy

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import BaggingRegressor


###### EDIT HERE #################################
def extract_features( net, img, code, rect, roi, roi_rect ):
    f = net( [roi] )
    return f

    '''
    #simple data augmentation
    roi_mirror = np.fliplr(roi).copy()
    f = net( [roi, roi_mirror] )
    return f
    '''

def regression( X, Y ):
    '''
    model = LinearRegression()
    model.fit( X, Y )
    return model
    '''
    # ensemble learning with bagging
    base_estimator = LinearRegression()
    n_estimators = 16
    max_features = 0.1
    model = BaggingRegressor( base_estimator=LinearRegression(), n_estimators=n_estimators, max_features=max_features )
    model.fit( X, Y )
    return model

##################################################

def code2label( code ):
    if( len(code) < 3 ):
        return None

    if( code[:3].lower() in ['dog', 'ant'] ):
        label = 0
    elif( code[:3].lower() in ['cat', 'bee'] ):
        label = 1
    else:
        label = None

    return label

def process_single_file(file, net):
    basename = os.path.basename(file)
    img = cv2.imread(file)
    if img is None:
        return None
    (code, rect), (roi, roi_rect) = detect_roi(img)
    if roi is not None:
        y_val = code2label(code)
        if y_val is not None:
            f = extract_features(net, img, code, rect, roi, roi_rect)
            return basename, code, y_val, f
    return None



def main( dir_imgs, network, model_name ):
    net = CNN(network)

    files = glob.glob( '{}/*'.format(dir_imgs) )
    X = None
    Y = None
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results = executor.map(lambda f: process_single_file(f,net), files)
        for res in results:
            if res is not None:
                basename, code, y_val, f=res
                nb_f = f.shape[0]
                y_arr = np.ones((nb_f,), dtype=np.int) * y_val

                X = f if (X is None) else np.concatenate((X,f), axis=0)
                Y = y_arr if (Y is None) else np.concatenate((Y,y_arr), axis=0)
                print(basename,code,y_arr)

    model = regression( X, Y )

    model_name = model_name + '_' + network + '.pkl'
    save_model( model_name, model )

    Ypred = model.predict( X )
    print( 'acc:', accuracy( Y, Ypred ) )

    for file in files:
        basename = os.path.basename(file)
        img = cv2.imread( file )
        (code, rect), (roi, roi_rect) = detect_roi( img )
        if( roi is not None ):
            x = net( [roi] )
            y = model.predict(x)
            print(basename, code, y[0])

    print( model_name )

if( __name__ == '__main__' ):
    parser = argparse.ArgumentParser(description='Train model')

    parser.add_argument('-n', '--network', default='alexnet')
    parser.add_argument('-m', '--model_name', default='model')
    parser.add_argument('-d', '--dir_imgs', default='ant-vs-bee/imgs_code/train/')

    args = parser.parse_args()
    main( **vars( args ) )
