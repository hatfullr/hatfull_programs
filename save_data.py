import numpy as np
import read_sph_data as rsd
import glob
import os


files = sorted(glob.glob("out*.sph"))
#if os.path.isdir("data"):
    #if os.path.isfile("data/filelist.txt"):
        #with open("data/filelist.txt",'r') as f:
        #    lines = f.read().splitlines()
        #    last_file = lines[-1]


temp,hdrtemp = rsd.read(files[0],return_header=True)
n = int(hdrtemp[0])
lenfiles = len(files)
dlen = len(temp[0])
shape = (lenfiles,n)

x = np.zeros(shape=shape)
y = np.zeros(shape=shape)
z = np.zeros(shape=shape)
am = np.zeros(shape=shape)
hp = np.zeros(shape=shape)
rho = np.zeros(shape=shape)
vx = np.zeros(shape=shape)
vy = np.zeros(shape=shape)
vz = np.zeros(shape=shape)
vxdot = np.zeros(shape=shape)
vydot = np.zeros(shape=shape)
vzdot = np.zeros(shape=shape)
u = np.zeros(shape=shape)
udot = np.zeros(shape=shape)
grpot = np.zeros(shape=shape)
meanmolecular = np.zeros(shape=shape)
cc = np.zeros(shape=shape)
divv = np.zeros(shape=shape)
if dlen > 18:
    ueq = np.zeros(shape=shape)
    tthermal = np.zeros(shape=shape)

sep0 = np.zeros(lenfiles)
t = np.zeros(lenfiles)
omega2 = np.zeros(lenfiles)
erad = np.zeros(lenfiles)

progress = 0.

for i in range(0,lenfiles):
    print("%3d%% %s" % (float(i+1)/lenfiles * 100., files[i]))
    data,hdr = rsd.read(files[i],return_header=True)
    
    x[i] = data[:,0]
    y[i] = data[:,1]
    z[i] = data[:,2]
    am[i] = data[:,3]
    hp[i] = data[:,4]
    rho[i] = data[:,5]
    vx[i] = data[:,6]
    vy[i] = data[:,7]
    vz[i] = data[:,8]
    vxdot[i] = data[:,9]
    vydot[i] = data[:,10]
    vzdot[i] = data[:,11]
    u[i] = data[:,12]
    udot[i] = data[:,13]
    grpot[i] = data[:,14]
    meanmolecular[i] = data[:,15]
    cc[i] = data[:,16]
    divv[i] = data[:,17]
    if dlen > 18:
        ueq[i] = data[:,18]
        tthermal[i] = data[:,19]
    
    sep0[i] = hdr[4]
    t[i] = hdr[9]
    omega2[i] = hdr[18]
    erad[i] = hdr[20]

if not os.path.isdir("data"):
    print "Creating data directory"
    os.mkdir("data")

print "Saving"
np.save("data/x",x)
np.save("data/y",y)
np.save("data/z",z)
np.save("data/am",am)
np.save("data/hp",hp)
np.save("data/rho",rho)
np.save("data/vx",vx)
np.save("data/vy",vy)
np.save("data/vz",vz)
np.save("data/vxdot",vxdot)
np.save("data/vydot",vydot)
np.save("data/vzdot",vzdot)
np.save("data/u",u)
np.save("data/udot",udot)
np.save("data/grpot",grpot)
np.save("data/meanmolecular",meanmolecular)
np.save("data/cc",cc)
np.save("data/divv",divv)

if dlen > 18:
    np.save("data/ueq",ueq)
    np.save("data/tthermal",tthermal)

np.save("data/sep0",sep0)
np.save("data/t",t)
np.save("data/omega2",omega2)
np.save("data/erad",erad)

with open("data/filelist.txt","w") as f:
    for i in files:
        f.write(i+"\n")
