import numpy as np
import glob
import sys

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

runit = 6.9598e10
munit = 1.9892e33

if len(sys.argv) > 1:
    user_input = " ".join(sys.argv[1:])
else:
    user_input = raw_input("Enter a file name(s) or pattern(s): ")
files = sorted(glob.glob(user_input))

fmt = " %-7s = %-15.7E g cm^-3"
for i in range(0,len(files)):
    coremass = np.sum(np.loadtxt(files[i],skiprows=2,max_rows=1)[-19:-14])
    data = np.loadtxt(files[i],skiprows=6)
    mass = data[:,2]
    idx = find_nearest(mass,coremass)
    Rc = 10.**data[idx][3]

    avgrhoc = np.mean(10.**data[:,5][::-1][:idx])
    
    rhoc = coremass / (4./3. * np.pi * Rc**3.)
    
    print(fmt % ("rhoc",rhoc*munit/runit**3.))
    print(fmt % ("<rho>_c",avgrhoc))
