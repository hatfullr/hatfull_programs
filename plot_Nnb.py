import glob
import numpy as np
import sys
import matplotlib.pyplot as plt

plt.style.use('supermongo')

if len(sys.argv) > 1:
    user_input = " ".join(sys.argv[1:])
else:
    user_input = raw_input("Enter file name: ")

files = sorted(glob.glob(user_input))

if len(files) > 1:
    raise Exception("Must use exactly one file")

files = files[0]

if files[:3] != "col" and files[-3:] != ".sph":
    raise Exception("Must use a file that begins with 'col' and ends with '.sph'")

data = np.loadtxt(files)

r = data[:,0]
Nnb = data[:,7]
u = data[:,14]

core_idx = np.where(u==0)[0]
idx = np.arange(len(data))
fig, ax = plt.subplots(dpi=200)

if len(core_idx) == 1:
    ax.scatter(r[core_idx],Nnb[core_idx],s=50,facecolors='none',edgecolors='k')
    ax.scatter(r[idx != core_idx],Nnb[idx != core_idx],s=1,color='k')
else:
    ax.scatter(r,Nnb,s=1,color='k')

ax.set_xlabel("$r_i$ [$R_\\odot$]")
ax.set_ylabel("$N_{nb,i}$")

plt.savefig("Nnb_vs_r_"+str(files[3:-4])+".png")

plt.show()
