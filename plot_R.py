import read_sph_data as rsd
import matplotlib.pyplot as plt
import glob
import numpy as np
import os.path

plt.style.use('supermongo')

def new_data_file():
    user_input = raw_input("Enter a file name(s) or pattern(s): ")
    files = sorted(glob.glob(user_input))
    dat = np.ndarray(shape=(len(files),2))
    fmt = "R = %- 15.7E"
    for i in range(0,len(files)):
        print "Reading",files[i]
        data, hdr = rsd.read(files[i],return_header=True)
        dat[i][0] = hdr[9]
        x = data[:,0]
        y = data[:,1]
        z = data[:,2]
        h = data[:,4]
        r = np.sqrt(x**2. + y**2. + z**2.)
        
        dat[i][1] = np.max(r+2.*h)
        print(fmt % (np.max(r+2.*h)))

    np.save("R_vs_t.npy",dat)
    return dat

if os.path.isfile("R_vs_t.npy"):
    user_input = raw_input("Data file 'R_vs_t.npy' detected. Overwrite? (y/n): ")
    if user_input == "y": dat = new_data_file()
    else: dat = np.load("R_vs_t.npy")
else: dat = new_data_file()

plt.plot(dat[:,0],dat[:,1],color='k')
plt.axhline(3.715,linestyle="--",color='k')
plt.xlabel("t")
plt.ylabel("max$\\left(r_i+2h_i\\right)$")
plt.show()
