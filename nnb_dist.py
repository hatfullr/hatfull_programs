import read_sph_data as rsd
import numpy as np

data = rsd.read("out0000.sph")
x = data[:,0]
y = data[:,1]
z = data[:,2]
h = data[:,4]

r = np.sqrt(x**2. + y**2. + z**2.)

ind = np.argmax(r+2.*h)

nn = 0
dx = x - x[ind]
dy = y - y[ind]
dz = z - z[ind]

dr = np.sqrt(dx**2. + dy**2. + dz**2.)

idx = np.where((dr < 2.*h[ind]) & (dr != 0))[0]
nn = len(idx)

print "nn =",nn
print "<dr> =",np.mean(dr[idx])
print "2.*h_i =",2.*h[ind]
print "<dr>/(2.*h_i) =",np.mean(dr[idx])/(2.*h[ind])

