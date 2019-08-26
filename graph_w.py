import numpy as np
import glob
import read_sph_data as rsd
import warnings
import matplotlib.pyplot as plt

warnings.filterwarnings('ignore')

simdir = "/home/hatfull/data/ulfhednar/relax/r022u_1.52M_2350Myr_100k_cubic_spline_hacked/"
datafiles = [min(glob.glob(simdir+"out*.sph")),max(glob.glob(simdir+"out*.sph"))]
moddir = "/home/hatfull/data/ulfhednar/starsev/s001u_V1309/models/"
modelfile = moddir+"m_1.52_t_2350.mod.muse"

#datafile = simdir+"out0398.sph"

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

def read_data(datafile):
    data_code, header = rsd.read(datafile,return_header=True)
    r_code = np.sqrt(data_code[:,0]**2. + data_code[:,1]**2. + data_code[:,2]**2.)
    data_code = data_code[np.argsort(r_code)] #Sort the data by radius so we can get mass coords.
    
    mencl = np.cumsum(data_code[:,3])
    r_code = np.sqrt(data_code[:,0]**2. + data_code[:,1]**2. + data_code[:,2]**2.)
    
    m_code = data_code[:,3]
    u_code = data_code[:,12] / G / Ms * Rs #ergs/g
    #w_code = data_code[:,14] / G / Ms * Rs #ergs/g
    w_code = -mencl / r_code / G / Ms * Rs

    t = header[9]
    return r_code[1:], mencl[1:], m_code[1:], u_code[1:], w_code[1:], t #Exclude the core

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

data_model = data_model[unqinds] #Remove duplicate entries except for the very last duplicate entry
m_model = data_model[:,0]
r_model = data_model[:,1]
u_model = data_model[:,20]
w_model = -m_model / r_model / G / Ms * Rs

r_code0, mencl0, m_code0, u_code0, w_code0, t0 = read_data(datafiles[0])
r_code1, mencl1, m_code1, u_code1, w_code1, t1 = read_data(datafiles[1])



plt.plot(r_model,np.log10(-w_model),color='k',label='EV 1D (766)')
plt.plot(r_code0,np.log10(-w_code0),color='r',label='SPH ($t='+str(t0)[:6]+'$)')
plt.plot(r_code1,np.log10(-w_code1),color='b',label='SPH ($t='+str(t1)[:6]+'$)')

plt.legend()

plt.xlabel("$r/R_{\\odot}$")
plt.ylabel("log$_{10}\ (-w)$ [ergs g$^{-1}$]")

plt.title(simdir.split("/")[-2]).set_position([0.5,1.05])


plt.savefig(simdir.split("/")[-2].split("_")[0]+"_w.png")

#plt.show()
