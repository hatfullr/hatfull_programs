import numpy as np
import read_sph_data as rsd
import sys
import glob

if len(sys.argv) > 1:
    user_input = " ".join(sys.argv[1:])
else:
    user_input = raw_input("Enter a file name(s) or pattern(s): ")
files = sorted(glob.glob(user_input))

fmt = " %-1s = %-d"
for i in range(0,len(files)):
    data = rsd.read(files[i])
    
    print(fmt % ("N",len(data)))
