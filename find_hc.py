import numpy as np
import read_sph_data as rsd
import warnings
import sys

#warnings.filterwarnings('ignore')

filename = raw_input("Enter a file name: ")
data = rsd.read(filename)

cid = np.where(data[:,12]==0)[0]
if len(cid) > 1:
    print("Something went wrong. Found more than 1 particle with u = 0.")
    sys.exit()

print("Core smoothing length is %- 15.7E Rsun" % (data[cid[0]][4]))
