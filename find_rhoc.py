import numpy as np
import read_sph_data as rsd
import warnings
import glob
import sys

warnings.filterwarnings('ignore')

runit = 6.9598e10
munit = 1.9892e33

if len(sys.argv) > 1:
    user_input = " ".join(sys.argv[1:])
else:
    user_input = raw_input("Enter a file name(s) or pattern(s): ")
files = sorted(glob.glob(user_input))
dat = np.ndarray(shape=(len(files),2))
fmt = " %-20s = %-15.7E g cm^-3"

for i in range(0,len(files)):
    data = rsd.read(files[i])
    Mc = data[0][3]
    hpc = data[0][4]
    rhoc = data[0][5]
    
    print(fmt % ("Mc/(4/3 pi (2hpc)^3)",Mc/(4./3. * np.pi * (2.*hpc)**3.)*munit/runit**3. ))
    print(fmt % ("rhoc",rhoc*munit/runit**3.))
