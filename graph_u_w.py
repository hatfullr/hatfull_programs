import numpy as np
import glob
import read_sph_data as rsd
import warnings
import matplotlib.pyplot as plt

warnings.filterwarnings('ignore')

simdir = "/home/hatfull/data/ulfhednar/relax/r024u_1.52M_2350Myr_100k_WC4_200Nnb_hacked/" #r024u
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

    return r_code[1:], mencl[1:], m_code[1:], u_code[1:], w_code[1:] #Exclude the core

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

r_code0, mencl0, m_code0, u_code0, w_code0 = read_data(datafiles[0])
r_code1, mencl1, m_code1, u_code1, w_code1 = read_data(datafiles[1])

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2,sharex='row',sharey='col',figsize=(8,8))


ax1.plot(r_model,np.log10(u_model),color='k')
ax1.plot(r_code0,np.log10(u_code0),color='r')
ax1.plot(r_code1,np.log10(u_code1),color='b')
ax1.set_ylim(13,15.5)
ax1.set_xlim(0,3.6)
ax1.set_xlabel('radius')
ax1.set_ylabel('u')

ax2.plot(r_model,np.log10(-w_model),color='k')
ax2.plot(r_code0,np.log10(-w_code0),color='r')
ax2.plot(r_code1,np.log10(-w_code1),color='b')
ax2.set_ylim(14.5,16)
ax2.set_xlim(0,3.6)
ax2.set_ylabel('w')
ax2.set_xlabel('radius')

ax3.plot(m_model,np.log10(u_model),color='k')
ax3.plot(mencl0,np.log10(u_code0),color='r')
ax3.plot(mencl1,np.log10(u_code1),color='b')
ax3.set_ylim(13,15.5)
ax3.set_xlim(0.181972,1.517267)
ax3.set_xlabel('mass')
ax3.set_ylabel('u')

ax4.plot(m_model,np.log10(-w_model),color='k')
ax4.plot(mencl0,np.log10(-w_code0),color='r')
ax4.plot(mencl1,np.log10(-w_code1),color='b')
ax4.set_ylim(14.5,16)
ax4.set_xlim(0.181972,1.517267)
ax4.set_ylabel('w')
ax4.set_xlabel('mass')

plt.suptitle(simdir.split("/")[-2].split("_")[0])
plt.tight_layout()
fig.subplots_adjust(top=0.94)

plt.savefig(simdir.split("/")[-2].split("_")[0]+"_u_w.png")

plt.show()
