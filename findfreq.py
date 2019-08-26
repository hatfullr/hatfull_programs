import numpy as np
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt

def findmaxima(x):
    x = np.convolve(x, np.ones((50,))/50, mode='same')
    localmax=np.array([],dtype=int)
    skiprun = False
    for i in range(1, len(x)-2):
        if not skiprun:
            if x[i-1] <= x[i] >= x[i+1]:
                localmax = np.append(localmax,i)
                if x[i] == x[i-1] or x[i] == x[i+1]:
                    skiprun = True
                    continue
        skiprun = False
    return localmax

    
data = np.loadtxt("energy0.sph")

t = data[:,0]
epot = data[:,1]
ekin = data[:,2]
eint = data[:,3]
etot = data[:,4]

allfreq = np.array([])
for j in [epot, ekin, eint, etot]:
    localmax = findmaxima(epot)
    freq = np.array([])
    for i in localmax[int(len(localmax)/2.):]:
        freq = np.append(freq, 1./(t[i+1]-t[i]))
    #print "Frequency is about",np.mean(freq)
    allfreq = np.append(allfreq,np.mean(freq))

print "Frequency is about", np.mean(allfreq)
    
#plt.scatter(t, epot,color='k',marker='.',s=1)
#for i in localmax:
#    plt.plot([t[i],t[i]],[max(epot),min(epot)],color='r')

#for i in argrelextrema(epot, np.greater,order=1):
#    plt.plot([t[i],t[i]],[max(epot),min(epot)],color='r')

plt.show()




