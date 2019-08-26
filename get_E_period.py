import numpy as np
import glob
import sys
from scipy.optimize import curve_fit
import os.path

def deriv(x,y):
    dx = np.diff(x)
    dy = np.diff(y)
    return dy/dx

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def f(t,w,sigma,A,phi):
    return A*np.exp(-w*sigma*t)*np.cos(w*np.sqrt(1-sigma**2.)*t+phi)


user_input = raw_input("Enter a file name: ")
datafile = glob.glob(user_input)
if len(datafile) <= 0:
    print "ERROR: Could not find file '"+datafile+"'."
    sys.exit()

fmt = "%15s = %- 15.7E +/- %- 15.7E"

b = ( [ -np.inf, 0., -np.inf, -np.inf ], [ np.inf, 1.0, np.inf, np.inf ] )

for i in range(0, len(datafile)):
    if os.path.isfile(datafile[i]):
        print "Reading '"+datafile[i]+"'."
    else: continue

    data = np.loadtxt(datafile[i])

    t = data[:,0]
    epot = data[:,1]
    ekin = data[:,2]
    eint = data[:,3]
    etot = data[:,4]
    stot = data[:,5]
    ajtot = data[:,6]
    com = data[:,-1]
    omeg = data[:,-2]

    idx = np.where(t > t[0]+10.)[0] # Skip the first bit b/c it screws up the fit
    ydata = eint - np.mean(eint) #Move the curve down to center it on about y = 0
    ydata = ydata[idx]
    xdata = t[idx]

    popt,pcov = curve_fit(f,xdata,ydata, bounds=b)#, p0=p0)
    perr = np.sqrt(np.diag(pcov))

    period = 2.*np.pi / popt[0]
    period_err = 2.*np.pi * np.abs(-1.*popt[0]**(-2.) * perr[0])

    print( fmt % ("Eint period", period, period_err))


    ydata = epot - np.mean(epot)
    ydata = ydata[idx]
    xdata = t[idx]
    
    popt,pcov = curve_fit(f,xdata,ydata,bounds=b)
    perr = np.sqrt(np.diag(pcov))

    period = 2.*np.pi / popt[0]
    period_err = 2.*np.pi * np.abs(-1.*popt[0]**(-2.) * perr[0])

    print( fmt % ("Epot period", period, period_err))

