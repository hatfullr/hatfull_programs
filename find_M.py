import numpy as np
import read_sph_data as rsd
import warnings

warnings.filterwarnings('ignore')

filename = raw_input("Enter a file name: ")
data = rsd.read(filename)

print("Total mass is %- 15.7E Msun" % (np.sum(data[:,3])))
