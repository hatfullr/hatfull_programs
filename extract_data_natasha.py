import numpy as np
import read_sph_data as rsd
import glob
from constants import *
import warnings
warnings.filterwarnings('ignore')

simdir="/home/hatfull/data/ulfhednar/relax/r040u_1.52M_2350Myr_50k_WC4_63_nnopt_1.5x_hp1/"

filenum = max(glob.glob(simdir+"col*.sph"))[-8:-4]
coldata = np.loadtxt(simdir+"col"+str(filenum)+".sph")
datafile = simdir+"out"+str(filenum)+".sph"

coldata = np.loadtxt(simdir+"col"+str(filenum)+".sph")
data, header = rsd.read(datafile,return_header=True)

rcol = coldata[:,0]
rdata = np.sqrt(data[:,0]**2. + data[:,1]**2. + data[:,2]**2.)

coldata = coldata[np.argsort(rcol)]
data = data[np.argsort(rdata)]

#Get data in cgs
x = coldata[:,10] / Rs
y = coldata[:,11] / Rs
z = coldata[:,12] / Rs
P = coldata[:,1] / Ms * Rs
rho = coldata[:,2] / Ms * Rs**3.
T= coldata[:,3]
#s =
u = coldata[:,14] / G / Ms * Rs
w = coldata[:,13] / G / Ms * Rs
g = coldata[:,8] / Rs
#kappa =

print("%15s"*9 % ("x_i","y_i","z_i","P_i","rho_i","T_i","u_i","w_i","g_i"))
print("%15s"*9 % ("[cm]","[cm]","[cm]","[dyne cm^-2]","[g cm^-3]","[K]","[ergs g^-1]","[ergs g^-1]","[cm s^-2]"))
for i in range(0, len(x)):
    print("%- 15.7E"*9 % (x[i],y[i],z[i],P[i],rho[i],T[i],u[i],w[i],g[i]))
