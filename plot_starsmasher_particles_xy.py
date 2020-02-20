import numpy as np
import read_sph_data as rsd
import matplotlib.pyplot as plt
import sys
import glob

plt.style.use('supermongo')

if len(sys.argv) > 1:
#    user_input = " ".join(sys.argv[1:])
    files = sys.argv[1:]
else:
    user_input = raw_input("Enter a file name(s) or pattern(s): ")
    files = sorted(glob.glob(user_input))


for i in range(0,len(files)):
    print(files[i])
    data = rsd.read(files[i])
    x = data[:,0]
    y = data[:,1]
    u = data[:,12]

    idxs = np.where(u == 0)[0]
    
    plt.scatter(x,y,color='k',s=1)
    plt.scatter(x[idxs],y[idxs],color='r',s=10)

    plt.gca().set_aspect('equal')
    
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()
    

