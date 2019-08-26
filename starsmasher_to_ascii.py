from __future__ import print_function # Allows python2 and python3 functionality
import numpy as np
import read_sph_data as rsd
import glob

tunit = 1.59353e3 / 60. / 60. / 24.

# This allows the program to be used by both python2 and python3
try:
    input = raw_input
except NameError:
    pass

filepattern = None
files = []
while len(files) == 0:
    if filepattern is None:
        filepattern = input("Enter file name(s) or patterns: ")
    try:
        filepattern = filepattern.split()
    except AttributeError:
        pass
    for pattern in filepattern:
        fs = sorted(glob.glob(pattern))
        if len(fs) > 0:
            for i in fs:
                files.append(i)
        else:
            print("ERROR: One or more file pattern not found")
            files = []
            filepattern = None
            break

data,hdr = rsd.read(files[0],return_header=True)
fmt = '%- 15.7E'
        
for i in range(0,len(files)):
    filename = files[i].replace(".sph",".txt")
    data,hdr = rsd.read(files[i],return_header=True)
    print("Writing",filename)
    np.savetxt(filename,data,fmt=fmt,header=str(hdr[9]*tunit),comments='')
