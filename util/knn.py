import numpy as np

class dist:
    def __init__( self, Y=None ):
        self.set_data( Y )

    def set_data( self, Y ):
        if( Y is None ):
            self.Y = None
            self.Y2= None
        else:
            self.Y = np.copy( Y ).transpose()
            self.Y2= ( self.Y * self.Y ).sum(axis=0)
            self.Y2= self.Y2.reshape( (1,)+self.Y2.shape )

    def __call__( self, X ):
        X2 = ( X * X ).sum(axis=1).reshape( (X.shape[0],1) )
        XY = np.matmul( X, self.Y )
        return X2 - 2*XY + self.Y2

class kNN:
    def __init__( self, Y=None, C=None ):
        self.set_data( Y, C )

    def set_data( self, Y, C ):
        self.dist = dist( Y )
        self.C = np.copy( C )

    def __call__( self, X, k=1 ):
        d = self.dist( X )
        r = np.argsort(d, axis=1)
        r = r[:,:k]
        return np.asarray([ [ self.C[ r[i,j] ] for j in range(r.shape[1]) ] for i in range(r.shape[0])])

if( __name__=='__main__' ):
    C = [0,0,0,1,1,1]
    Y = np.random.rand( 6, 32 )

    X = np.random.rand( 2, 32 )

    knn = kNN( Y, C )
    nn = knn( X, 2 )
    print( nn )
