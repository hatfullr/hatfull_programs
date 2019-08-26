import numpy as np
import read_sph_data as rsd
import matplotlib.pyplot as plt
from scipy.spatial import distance
import time
import itertools
import sys

plt.style.use('supermongo')

#filename = raw_input("Enter a file name: ")
filename = "out0100.sph"
data, header = rsd.read(filename, return_header=True)

#order the data
r = np.sqrt(data[:,0]**2. + data[:,1]**2. + data[:,2]**2.)
data = data[np.argsort(r)]

x = data[:,0]
y = data[:,1]
z = data[:,2]
hp = data[:,4]

r = np.sqrt(x**2. + y**2. + z**2.)

xyz = data[:,0:3]

rhpplus = r + 2.*hp
rhpminus = abs(r - 2.*hp)

threshold = 10000
i = 0
ntot = len(data)
Nnb = np.zeros(ntot)
innervalid = 0
while i != ntot:
    # Encapsulate threshold particles
    en0 = i
    en1 = i + threshold
    encap = range(en0, en1)

    # Calculate distances of encapsulated particles
    dists = distance.squareform(distance.pdist(xyz[encap]))

    # Find the particle whose kernel is closest to the outer encapsulation
    # radius, but not further than it
    outervalid = np.where(r[encap]+2.*hp[encap] <= r[en1])[0][-1]

    # Save the valid Nnb's
    for j in range(innervalid,outervalid):
        Nnb[j] = len(np.where(dists[j-innervalid] < 2.*hp[j])[0])
        #print len(np.where(dists[j-innervalid] < 2.*hp[j])[0])
    
    # Find the encapsulated, but not valid particles
    notvalid = range(outervalid, en1)

    # Find the r value for the inner-most edge of the notvalid particles' kernels
    r_low_notvalid = min(r[notvalid] - 2.*hp[notvalid])

    # Find the particle with the closest central r value to this spot
    r_closest_low_notvalid = np.where(r <= r_low_notvalid)[0][-1]

    #print i, str(min(encap))+" to "+str(max(encap)), len(np.where(Nnb > 0)[0])
    print en0, en1
    print innervalid, outervalid, r_closest_low_notvalid, r_low_notvalid
    print ""
    i = r_closest_low_notvalid
    innervalid = r_closest_low_notvalid

for j in range(0,len(data),10000):
    outeredge = max(r[j:j+10000])
    print rhp >= outeredge
    limit = np.argmax(rhp >= outeredge)
    d1 = distance.pdist(xyz[j:j+10000])
    square = distance.squareform(d1)
    print limit
    sys.exit()
    for i in range(0,len(square)):
        print len(np.where(square[i] < 2.*hp[i])[0])
#print len(np.where(square < 2.*hp[:10000])[0])


t0 = time.time()
for i in range(0,int(header[0])):
    dr = np.sqrt((x-x[i])**2. + (y-y[i])**2. + (z-z[i])**2.)
    neighbors = np.where(dr < 2.*hp[i])[0]

    #filt1 = np.where(abs(x-x[i]) < 2.*hp[i])[0]
    #filt2 = np.where(abs(y[filt1]-y[i]) < 2.*hp[i])[0]
    #filt3 = np.where(abs(z[filt2]-z[i]) < 2.*hp[i])[0]
    #dr = np.sqrt((x[filt3]-x[i])**2. + (y[filt3]-y[i])**2. + (z[filt3]-z[i])**2.)
    #dr = np.sqrt((x-x[i])**2. + (y-y[i])**2. + (z-z[i])**2.)
    #neighbors = np.where(dr < 2.*hp[i])[0]
    #print i, len(neighbors)

    #plt.scatter(x[neighbors],y[neighbors],s=1,color='k')
    #plt.scatter(x[i],y[i],s=1,color='r')
    #circle = plt.Circle((x[i],y[i]),2.*hp[i],fill=False,edgecolor='r')
    #plt.gca().add_artist(circle)
    #plt.gca().set_aspect('equal')
    #plt.show()
t1 = time.time()

print "Total elapsed time =",t1-t0


