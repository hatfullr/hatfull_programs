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
fmt = " %-1s = %-15.7E %s"
for i in range(0,len(files)):
    print "Reading",files[i]
    data,hdr = rsd.read(files[i],return_header=True)

    t = hdr[9]
    
    print(fmt % ("t",t,"code units"))
    print(fmt % ("t",t*np.sqrt(runit**3./gravconst/munit),"seconds"))
    print(fmt % ("t",t*np.sqrt(runit**3./gravconst/munit)/60.,"minutes"))
    print(fmt % ("t",t*np.sqrt(runit**3./gravconst/munit)/60./60.,"hours"))
    print(fmt % ("t",t*np.sqrt(runit**3./gravconst/munit)/60./60./24.,"days"))
    print(fmt % ("t",t*np.sqrt(runit**3./gravconst/munit)/60./60./24./365.,"years"))


