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

data_model_orig = data_model[unqinds] #Remove duplicate entries except for the very last duplicate entry
envcutoffs = [ data_model_orig[-1][0] - 0.1, data_model_orig[-1][0] - 0.2, data_model_orig[-1][0] - 0.5 ]

data_code_orig, header = rsd.read(datafile,return_header=True)
r_code = np.sqrt(data_code_orig[:,0]**2. + data_code_orig[:,1]**2. + data_code_orig[:,2]**2.)
data_code_orig = data_code_orig[np.argsort(r_code)] #Sort the data by radius just for ease.
    
mencl_orig = np.cumsum(data_code_orig[:,3])


print "Files:"
print "     Data file: ",datafile
print "     Model file:",modelfile
print ""
print "Calculating energies for only the outer 10% of the envelope..."
print ""
print "Time =",header[9],"code units"
print ""



for envcutoff in envcutoffs:

    print "Energies for M(r) =", envcutoff,"Msun"
    
    data_model = data_model_orig[np.where(data_model_orig[:,0] >= envcutoff)]

    #data_code, header = rsd.read(datafile,return_header=True)
    #r_code = np.sqrt(data_code[:,0]**2. + data_code[:,1]**2. + data_code[:,2]**2.)
    #data_code = data_code[np.argsort(r_code)] #Sort the data by radius just for ease.
    
    #mencl = np.cumsum(data_code[:,3])
    
    data_code = data_code_orig[np.where(mencl_orig >= envcutoff)] #Get outer 10% of envelope
    mencl = mencl_orig[np.where(mencl_orig >= envcutoff)]
    
    r_code = np.sqrt(data_code[:,0]**2. + data_code[:,1]**2. + data_code[:,2]**2.)

    m_code = data_code[:,3]
    u_code = data_code[:,12] / G / Ms * Rs
    #w_code = data_code[:,14] / G / Ms * Rs
    w_code = -mencl / r_code / G / Ms * Rs
    h_code = data_code[:,4]
    
    m_model = data_model[:,0]
    r_model = data_model[:,1]
    u_model = data_model[:,20]
    w_model = -m_model / r_model / G / Ms * Rs



    
    Epot_code = np.sum(w_code*m_code/Ms)
    Eint_code = np.sum(u_code*m_code/Ms)
    
    Epot_code = simps(w_code,x=mencl/Ms)
    Eint_code = simps(u_code,x=mencl/Ms)
    
    Epot_model = simps(w_model,x=m_model/Ms)
    Eint_model = simps(u_model,x=m_model/Ms)

    Ebind_code = Epot_code + Eint_code
    Ebind_model = Epot_model + Eint_model
    

    print("%20s = %- 15.7E ergs" % ("Ebind_SPH",Ebind_code))
    print("%20s = %- 15.7E ergs" % ("Ebind_model",Ebind_model))

    print ""
