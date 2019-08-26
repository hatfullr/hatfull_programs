import numpy as np
import read_sph_data as rsd
import glob
import sys

if len(sys.argv) > 1:
    user_input = sys.argv[1:]
else:
    user_input = raw_input("Enter file name(s) or pattern(s): ").split(" ")

datafiles = []
for i in user_input:
    files = sorted(glob.glob(i))
    for f in files:
        datafiles.append(f)

for i in range(0,len(datafiles)):
    data = rsd.read(datafiles[i],lines=1)
    
