import numpy as np
from fastfileread import read_starsmasher
import sys
from glob import glob

if len(sys.argv) > 1:
    files = sorted(sys.argv[1:])
else:
    user_input = raw_input("Enter a file name(s) or pattern(s): ")
    files = sorted(glob(user_input))

data, headers = read_starsmasher(files,return_headers=True)

fmt = " erad = %15.7E"
for h in headers:
    print(fmt % h['erad'])
    
