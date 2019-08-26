import numpy as np
from scipy.integrate import *
import glob
import read_sph_data as rsd

import warnings
warnings.filterwarnings('ignore')

simdir = "/home/hatfull/data/ulfhednar/relax/r022u_1.52M_2350Myr_100k_cubic_spline_hacked/"
moddir = "/home/hatfull/data/ulfhednar/starsev/s001u_V1309/models/"
datafile = simdir+"out1103.sph"
modelfile = moddir+"m_1.52_t_2350.mod.muse"

a = np.float64(7.5657e-15) #erg/cm^3/K^4
k = np.float64(1.38064852e-16) #erg/K
m_H = np.float64(1.6737236e-24) #g
g = np.float64(1./1000.) #kg
cm = np.float64(1./100.) #m
s = np.float64(1.)
J = np.float64(g * cm**2. / s**2.) #Joules
G = np.float64(1./(6.67408e-11 / cm**3. * g * s**2.)) #Gravitational cosntant in cgs
Ms = np.float64(1./(1.9891e30 / g)) #Mass of the sun in cgs
Rs = np.float64(1./(6.9599e8 / cm)) #Radius of the sun in cgs
gamma = 5./3.

data_code, header = rsd.read(datafile,return_header=True)

r_code = np.sqrt(data_code[:,0]**2. + data_code[:,1]**2. + data_code[:,2]**2.)
data_code = data_code[np.argsort(r_code)] #Sort the data by radius just for ease.

data_model = np.loadtxt(modelfile)
data_model = data_model[np.where(data_model[:,0] > 0.181972)] #Exclude the core

#We need to remove entries that have duplicate values of M so we can integrate
mockdata = data_model[:,0]
unqinds = np.array([],dtype=np.int32)
for i in range(0, len(mockdata)-1):
    if mockdata[i] != mockdata[i+1]:
        unqinds = np.append(unqinds,i)

if mockdata[-2] == mockdata[-1]:
    unqinds = np.append(unqinds,-1)

data_model = data_model[unqinds]
    
m_code = data_code[:,3]
r_code = np.sqrt(data_code[:,0]**2. + data_code[:,1]**2. + data_code[:,2]**2.)

mencl = np.cumsum(data_code[:,3])

u_code = data_code[:,12][1:] / G / Ms * Rs #Exclude the core
#w_code = data_code[:,14][1:] / G / Ms * Rs
w_code = - mencl / r_code / G / Ms * Rs
w_code = w_code[1:] #Exclude the core

mencl = mencl[1:] #Exclude the core

m_model = data_model[:,0]
r_model = data_model[:,1]
u_model = data_model[:,20]
w_model = -m_model / r_model / G / Ms * Rs

#Epot_code = np.sum(w_code*m_code/Ms)
#Eint_code = np.sum(u_code*m_code/Ms)

Epot_code = simps(w_code,x=mencl/Ms)
Eint_code = simps(u_code,x=mencl/Ms)

Epot_model = simps(w_model,x=m_model/Ms)
Eint_model = simps(u_model,x=m_model/Ms)

print ""
print "Files:"
print "     Data file: ",datafile
print "     Model file:",modelfile
print ""
print "Time =",header[9],"code units"
print ""
print("%10s = %- 15.7E ergs" % ("Epot_SPH",Epot_code))
print("%10s = %- 15.7E ergs" % ("Epot_SPH",Eint_code))
print("%10s = %- 15.7E ergs" % ("Epot_model",Epot_model))
print("%10s = %- 15.7E ergs" % ("Epot_model",Eint_model))
print ""
print "-"*57
print '| {:^7} | {:^20} | {:^20} |'.format("","1/2 Epot [ergs]","Eint [ergs]")
print '|'+"-"*9+"|"+"-"*22+"|"+"-"*22+"|"
print '| {:>7} | {:^20} | {:^20} |'.format("SPH",Epot_code/2.,Eint_code)
print '|'+"-"*9+"|"+"-"*22+"|"+"-"*22+"|"
print '| {:>7} | {:^20} | {:^20} |'.format("model",Epot_model/2.,Eint_model)
print "-"*57

#print ""
#print ""
#print "    M [Msun]","     R [Rsun]","    u [erg/g]","    w [erg/g]"
#for i in range(0, len(w_model)):
#    print(4*" %- 10E" % (m_model[i],r_model[i],u_model[i],w_model[i]))

