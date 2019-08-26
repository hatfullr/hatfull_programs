import numpy as np
import glob
import read_sph_data as rsd
import warnings
from constants import *

warnings.filterwarnings('ignore')

simdir = "/home/hatfull/data/ulfhednar/dynamical/d003u_b002u_1.195M_0.32M_40k_1_1.2G0.32C0.32D_ncooling1/"
datafiles = [max(glob.iglob(simdir+'out*.sph'))]

for datafile in datafiles:
    # See get_ebind.f for data file format.
    #data_code = np.loadtxt(datafile)
    data_code,header = rsd.read(datafile,return_header=True,fmt_extra='f8,f8,f8',size_extra=24) #skip_end_junk=1 because of temp at the end, which I manually added
    r_code = np.sqrt(data_code[:,0]**2. + data_code[:,1]**2. + data_code[:,2]**2.)
    data_code = data_code[np.argsort(r_code)] #Sort the data by radius just for ease
    
    r_code = np.sqrt(data_code[:,0]**2. + data_code[:,1]**2. + data_code[:,2]**2.)
    
    m_code = data_code[:,3]
    v2_code = data_code[:,6]**2. + data_code[:,7]**2. + data_code[:,8]**2.
    u_code = data_code[:,12] / G / Ms * Rs
    
    w_code = data_code[:,14] / G / Ms * Rs

    ekin_code = 0.5*np.sqrt(v2_code) / G /Ms *Rs
    etot_code = 0.5*v2_code + u_code + w_code
    
    
    print("%15s = %- 11.7f Msun" % ("Total Mass", np.sum(m_code)))
    print("%15s = %- 11.7f Msun" % ("Bound Mass",np.sum(m_code[np.where(etot_code < 0)])))
    print("%15s = %- 11.7f Msun" % ("Unbound Mass",np.sum(m_code[np.where(etot_code >= 0)])))
    
