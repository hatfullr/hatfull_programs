import numpy as np
import read_sph_data as rsd
import matplotlib.pyplot as plt
import sys
import glob

plt.style.use('supermongo')

if len(sys.argv) > 1:
    user_input = " ".join(sys.argv[1:])
else:
    user_input = raw_input("Enter a file name(s) or pattern(s): ")
files = sorted(glob.glob(user_input))

for i in range(0,len(files)):
    data = rsd.read(files[i])
    x = data[:,0]
    z = data[:,2]

    plt.scatter(x,z,color='k',s=1)

    plt.xlabel("x")
    plt.ylabel("z")
    plt.show()
    

