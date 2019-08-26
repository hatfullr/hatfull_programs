import numpy as np
import read_sph_data as rsd
import warnings

warnings.filterwarnings('ignore')

filename = raw_input("Enter a file name: ")
data = rsd.read(filename)

print("Core smoothing length is %- 15.7E Msun" % (data[0][4]))
