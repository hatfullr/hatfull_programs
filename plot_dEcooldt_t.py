import numpy as np
import read_sph_data as rsd
import warnings
from constants import *
import matplotlib.pyplot as plt

warnings.filterwarnings('ignore')

def deriv(x,y):
    d = np.array([])
    for i in range(0, len(x)-1):
        d = np.append(d, (y[i+1]-y[i])/(x[i+1]-x[i]))

    return d

simdir = "/home/hatfull/data/ulfhednar/dynamical/d003u_b002u_1.195M_0.32M_40k_1_1.2G0.32C0.32D_ncooling1/"

t = np.load("data/t.npy")
erad = np.load("data/erad.npy")

erad = erad / G / Ms**2. * Rs
t = t / codeunits * days

deraddt = deriv(t/days,erad)

plt.plot(t[:-1],deraddt,color='k')
plt.xlabel("time [days]")
plt.ylabel("$dE_{\\rm{rad}}/dt$ [ergs s$^{-1}$]")

plt.title(simdir.split("/")[-2],y=1.05)
plt.tight_layout()

plt.savefig(simdir.split("/")[-2].split("_")[0]+"_deraddt_t.png")

plt.show()

