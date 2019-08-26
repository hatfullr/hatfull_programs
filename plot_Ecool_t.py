import numpy as np
import read_sph_data as rsd
import warnings
from constants import *
import matplotlib.pyplot as plt

warnings.filterwarnings('ignore')

simdir = "/home/hatfull/data/ulfhednar/dynamical/d003u_b002u_1.195M_0.32M_40k_1_1.2G0.32C0.32D_ncooling1/"

t = np.load("data/t.npy")
erad = np.load("data/erad.npy")

erad = erad / G / Ms**2. * Rs
t = t / codeunits * days

plt.plot(t,erad/1.e45,color='k')
plt.xlabel("time [days]")
plt.ylabel("$E_{\\rm{rad}}$ [$10^{45}$ ergs s$^{-1}$]")

plt.title(simdir.split("/")[-2])
plt.tight_layout()

plt.savefig(simdir.split("/")[-2].split("_")[0]+"_erad_t.png")

plt.show()

