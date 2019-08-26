import read_sph_data as rsd
import glob
import numpy as np
import sys

gravconst = 6.67390e-08
runit = 6.9598e10
munit = 1.9892e33

if len(sys.argv) > 1:
    user_input = " ".join(sys.argv[1:])
else:
    user_input = raw_input("Enter a file name(s) or pattern(s): ")

files = sorted(glob.glob(user_input))
dat = np.ndarray(shape=(len(files),2))
fmt = " %-1s = %-15.7E"
for i in range(0,len(files)):
    print "Reading",files[i]
    data = rsd.read(files[i])

    # Organize particles by radii first
    m = data[:,3]
    energy = data[:,12] # specific internal energy

    U = np.sum(energy*m)*gravconst*munit**2./runit #in cgs

    print(fmt % ("U",U))

