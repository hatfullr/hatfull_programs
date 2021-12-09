# Simpson's rule integration
import numpy as np

def simps(x,y):
    dx = np.diff(x)
    result = np.full(len(y)-1,np.nan)
    y1 = y[0]
    d = 0
    for i,y2 in enumerate(y[1:]):
        d += 0.5*(y1+y2)*dx[i]
        result[i] = d
        y1 = y2
    return result
