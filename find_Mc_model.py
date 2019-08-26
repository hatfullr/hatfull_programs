import numpy as np
import glob
import sys

runit = 6.9598e10
munit = 1.9892e33

if len(sys.argv) > 1:
    user_input = " ".join(sys.argv[1:])
else:
    user_input = raw_input("Enter a file name(s) or pattern(s): ")
files = sorted(glob.glob(user_input))

fmt = " %-2s = %-15.7E Msun"
for i in range(0,len(files)):
    coremass = np.sum(np.loadtxt(files[i],skiprows=2,max_rows=1)[-19:-14])

    print(fmt % ("Mc",coremass))
