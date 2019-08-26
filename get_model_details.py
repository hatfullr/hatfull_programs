import numpy as np
from constants import *

moddir = "/home/hatfull/data/ulfhednar/starsev/s001u_V1309/models/"
modelfile = moddir+"m_1.52_t_2350.mod.muse"

data_model = np.loadtxt(modelfile)

r_model = data_model[:,1] # in Rsun
m_model = data_model[:,0] # in Msun
T_model = data_model[:,4] # in K

print("   R = %5.5g Rsun" % (r_model[-1]))
print("   M = %5.5g Msun" % (m_model[-1]))
print("Teff = %5.5g Msun" % (T_model[-1]))

