import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np
import glob
import sys
import itertools

plt.style.use('supermongo')

if len(sys.argv) > 1:
    user_input1 = sys.argv[1:2][0]
    user_input2 = sys.argv[2:]
else:
    user_input1 = raw_input("Enter parent file name: ")
    user_input2 = raw_input("Enter data file name(s) or pattern(s): ")
    user_input2 = user_input2.split(" ")

modelfile = glob.glob(user_input1)[0]
colfiles = []
for i in user_input2:
    files = glob.glob(i)
    for j in files:
        colfiles.append(j)
colfiles = sorted(colfiles)

fig = plt.figure()

gs1 = GridSpec(4,2)
gs2 = GridSpec(3,2)
ax = []
ax.append(fig.add_subplot(gs2[0,0]))
ax.append(fig.add_subplot(gs2[1,0],sharex=ax[0]))
ax.append(fig.add_subplot(gs2[2,0],sharex=ax[0]))
ax.append(fig.add_subplot(gs1[0,1],sharex=ax[0]))
ax.append(fig.add_subplot(gs1[1,1],sharex=ax[0]))
ax.append(fig.add_subplot(gs1[2,1],sharex=ax[0]))
ax.append(fig.add_subplot(gs1[3,1],sharex=ax[0]))

plt.subplots_adjust(wspace=0.5,bottom=0.1)

ax[6].set_xlabel('r')
ax[2].set_xlabel('r')
ax[0].set_ylabel('A')
ax[1].set_ylabel('P')
ax[2].set_ylabel('$\\rho$')
ax[3].set_ylabel('$m_i$')
ax[4].set_ylabel('$h_i$')
ax[5].set_ylabel('$N_N$')
ax[6].set_ylabel('radial g, a$_{\\mathrm{hydro}}$')

data = np.loadtxt(modelfile)
r2 = data[:,0]
p2 = data[:,1]
rho2 = data[:,2]
temp = data[:,3]
mu = data[:,4]
a2 = p2/rho2**(5./3.)

ax[2].plot(r2,np.log10(rho2),color='r')
ax[0].plot(r2,np.log10(a2),color='r')
ax[1].plot(r2,np.log10(p2),color='r')

for i in range(0,len(colfiles)):
    print "Reading",colfiles[i]
    num_lines = sum(1 for line in open(colfiles[i]))
    if num_lines > 100000: # Plot a maximum of 100000 points
        cull = int(float(num_lines)/100000.) + 1
    else:
        cull = 1

    with open(colfiles[i]) as f:
        data = np.genfromtxt(itertools.islice(f,0,None,cull),dtype=float,usecols=(0,1,2,5,6,7,8,9))

    r1 = data[:,0]
    p1 = data[:,1]
    rho1 = data[:,2]
    am1 = data[:,3]
    h1 = data[:,4]
    nn1 = data[:,5]
    g1 = data[:,6]
    ah1 = data[:,7]

    idx = np.where(p1>0)[0]
    a1 = p1[idx]/rho1[idx]**(5./3.)

    scats = []
    scats.append(ax[6].scatter(r1,g1,color='g',s=1))
    scats.append(ax[6].scatter(r1,ah1,color='b',s=1))
    scats.append(ax[3].scatter(r1,np.log10(am1),color='k',s=1))
    scats.append(ax[4].scatter(r1,h1,color='k',s=1))
    scats.append(ax[5].scatter(r1,nn1,color='k',s=1))
    scats.append(ax[2].scatter(r1,np.log10(rho1),color='k',s=1))
    scats.append(ax[0].scatter(r1[idx],np.log10(a1),color='k',s=1))
    scats.append(ax[1].scatter(r1,np.log10(p1),color='k',s=1))

    num = colfiles[i].split("/")[-1][3:7]
    title = fig.text(0.1,0.97,'t = '+str(int(num)*1.8e-2)+' days',ha='center',va='center')
    
    plt.savefig("pa_"+num+".png")

    for k in scats:
        k.remove()

    title.remove()
    
