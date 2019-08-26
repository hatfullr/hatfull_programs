import numpy as np
import glob
import read_sph_data as rsd
import warnings
from constants import *
import matplotlib.pyplot as plt
import os
import time

warnings.filterwarnings('ignore')

simdir = "/home/hatfull/data/ulfhednar/dynamical/d003u_b002u_1.195M_0.32M_40k_1_1.2G0.32C0.32D_ncooling1/"
datafiles = sorted(glob.iglob(simdir+'out*.sph'))

m = np.load("data/m.npy")
vx = np.load("data/vx.npy")
vy = np.load("data/vy.npy")
vz = np.load("data/vz.npy")
t = np.load("data/t.npy")

if not os.path.isfile("data/e_particle.npy"):
    print "Calculating e_particle..."
    start = time.time()
    u = np.load("data/u.npy")
    w = np.load("data/grpot.npy")
    e_particle = 0.5 * (vx**2. + vy**2. + vz**2.) + w + u # In code units
    print("--- %s seconds ---" % (time.time() - start))
    print ""
    np.save("data/e_particle",e_particle)
else:
    e_particle = np.load("data/e_particle.npy")


m_ejected = np.array([])
Ekin_ejected = np.array([])

for i in range(0, len(m)):
    ejected = np.where(e_particle[i] > 0)[0]
    bound = np.where(e_particle[i] <= 0)[0]
    m_ejected = np.append(m_ejected,np.sum(m[i][ejected]))
    Ekin_ejected = np.append(Ekin_ejected, np.sum(0.5 * m[i][ejected] * (vx[i][ejected]**2. + vy[i][ejected]**2. + vz[i][ejected]**2.)))


Ekin_ejected = Ekin_ejected / G / Ms**2. * Rs * 1.0e-46 #In 10^(-46) ergs "eunit"


fig, (ax1, ax2) = plt.subplots(2,1,sharex=True,figsize=(8,8))

ax1.plot(t/codeunits * days, Ekin_ejected,color='k')
ax2.plot(t/codeunits * days, m_ejected,color='k')

ax1.set_ylabel("$E_{\\rm{kin}}^{\\infty}$ [$10^{46}$ ergs]")
ax2.set_ylabel("$m_{\\rm{ejecta}}$ [$M_{\\odot}$]")

ax2.set_xlabel("time [days]")

ax1.tick_params(axis='both',which='both',direction='in',top=True,bottom=True,left=True,right=True)
ax2.tick_params(axis='both',which='both',direction='in',top=True,bottom=True,left=True,right=True)

plt.tight_layout()
plt.suptitle(simdir.split("/")[-2])
fig.subplots_adjust(top=0.95,hspace=0)

plt.savefig(simdir.split("/")[-2].split("_")[0]+"_Ekin_infty_mejecta_time.png")

plt.show()
