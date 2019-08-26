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
fmt = " %-2s = %-15.7E Rsun"

for i in range(0,len(files)):
    data = rsd.read(files[i])
    hpc = data[0][4]
    
    print(fmt % ("Rc",2.*hpc))
