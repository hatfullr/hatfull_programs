from glob import glob
import numpy as np
import sys
import matplotlib.pyplot as plt

plt.style.use('supermongo')

if len(sys.argv) > 1:
    user_input = " ".join(sys.argv[1:])
else:
    user_input = raw_input("Enter file name(s) or pattern(s): ")

user_input = user_input.split(" ")

files = []
for f in user_input:
    for f1 in sorted(glob(f)):
        files.append(f1)

for f in files:
    if f.split("/")[-1][:3] != "col" and f.split("/")[-1][-3:] != ".sph":
        raise Exception("File '"+f+"' does not match the file name requirements. Must use a file that begins with 'col' and ends with '.sph'")

fig, ax = plt.subplots(dpi=200)

for f in range(0,len(files)):
    data = np.loadtxt(files[f])
    r = data[:,0]
    Nnb = data[:,7]
    u = data[:,14]

    core_idx = np.where(u==0)[0]
    idx = np.arange(len(data))

    label = files[f][-15:]
    
    if len(core_idx) == 1:
        sc = ax.scatter(r[idx != core_idx],Nnb[idx != core_idx],s=1,label=label,zorder=len(files)-f)
        c = sc.get_facecolors()
        ax.scatter(r[core_idx],Nnb[core_idx],s=50,facecolors='none',edgecolors=c,zorder=len(files)-f)
    else:
        ax.scatter(r,Nnb,s=1,label=label,zorder=len(files)-f)

ax.legend()
        
ax.set_xlabel("$r_i$ [$R_\\odot$]")
ax.set_ylabel("$N_{nb,i}$")

plt.savefig("Nnb_vs_r_compare.png")

plt.show()
