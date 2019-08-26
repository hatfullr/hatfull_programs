import numpy as np
import matplotlib.pyplot as plt
import random

plt.style.use("supermongo")

N = 10 # Number of particles
nxmapmax = 499
nymapmax = 499
nzmap = 416

# Set up our grid
xminmap = 0  # minimum x coordinate of grid
xmaxmap = 10 # maximum x coordinate of grid
yminmap = 0  # minimum y coordinate of grid
ymaxmap = 10 # maximum y coordinate of grid

dx_grid = xmaxmap - xminmap
dy_grid = ymaxmap - yminmap

nxmap = 3 # How many grid cells to use in x direction
nymap = 3 # How many grid cells to use in y direction

hxmap=(xmaxmap-xminmap)/float(nxmap-1) # Size of cell in x
hymap=(ymaxmap-yminmap)/float(nymap-1) # Size of cell in y

zmin = np.zeros(shape=(nxmapmax,nymapmax))
zmax = np.zeros(shape=(nxmapmax,nymapmax))

h1 = np.zeros(shape=(nxmapmax,nymapmax))

# Set up some fake particle data
x = np.zeros(N)
y = np.zeros(N)
z = np.zeros(N)
hp = np.zeros(N)
for i in range(0, N):
    x[i] = random.uniform(xminmap-0.1*dx_grid,xmaxmap+0.1*dx_grid)
    y[i] = random.uniform(yminmap-0.1*dy_grid,ymaxmap+0.1*dy_grid)
    z[i] = random.uniform(-5.,5.)
    hp[i] = 0.5*random.uniform(0.01, 5.)



# Find limits of integration:
for j in range(0,nymap):
    for i in range(0, nxmap):
        zmin[i][j] = 1.e30
        zmax[i][j]=-1.e30

for ip in range(0,N):
    yposmin=y[ip]-2*hp[ip]
    yposmax=y[ip]+2*hp[ip]
    jmin=max(int((yposmin-yminmap)/hymap+2),1)
    jmax=min(int((yposmax-yminmap)/hymap+1),nymap)

#    print(("%7d " + "%- 15.7E "*3 + "%7d "*2) % (ip, 2*hp[ip], yposmin, yposmax, jmin, jmax))


    for j in range(jmin,jmax):
        ypos = (j-1)*hymap+yminmap
        maxdx = (4*hp[ip]**2. - (y[ip]-ypos)**2.)**0.5
        xposmin = x[ip]-maxdx
        xposmax = x[ip]+maxdx
        imin=max(int((xposmin-xminmap)/hxmap+2),1)
        imax=min(int((xposmax-xminmap)/hxmap+1),nxmap)

        for i in range(imin,imax):
            xpos=(i-1)*hxmap+xminmap
            maxdz=(4*hp[ip]**2.-(x[ip]-xpos)**2.-(y[ip]-ypos)**2.)**0.5
            if z[ip]-maxdz < zmin[i][j]:
                zmin[i][j] = z[ip]-maxdz
                h1[i][j] = hp[ip]
            zmax[i][j] = max(zmax[i][j],z[ip]+maxdz)
#            print("%- 9.4f "*5 % (x[ip],y[ip],z[ip],zmin[i][j],zmax[i][j]))
            
# Plot the grid
#for i in range(xminmap,xmaxmap+1):
#    plt.plot([xminmap,xmaxmap],[i,i],color='k')
#    plt.plot([i,i],[yminmap,ymaxmap],color='k')

# Plot the particles
for i in range(0,N):
    particle = plt.Circle((x[i],y[i]),2*hp[i],color='r',alpha=1./N)
    border = plt.Circle((x[i],y[i]),2*hp[i],facecolor='none', edgecolor='k')
    plt.axes().add_artist(particle)
    plt.axes().add_artist(border)
plt.scatter(x,y,color='k',marker='.')

plt.xlabel("x")
plt.ylabel("y")
plt.tight_layout()
plt.xlim(-1,11)
plt.ylim(-1,11)
#plt.axes().set_aspect('equal')
plt.savefig('fakeSPH_nogrid')

# Plot the grid
for i in range(0,nxmap):
    ycoord = i*float(xmaxmap-xminmap)/(nxmap-1.)
    plt.plot([xminmap,xmaxmap],[ycoord,ycoord],color='k')

for i in range(0,nymap):
    xcoord = i*float(ymaxmap-yminmap)/(nymap-1.)
    plt.plot([xcoord,xcoord],[yminmap,ymaxmap],color='k')


# Annotate the grid marks
for i in range(0,nxmap):
    xcoord = i*float(ymaxmap-yminmap)/(nymap-1.)
    for j in range(0,nymap):
        ycoord = j*float(xmaxmap-xminmap)/(nxmap-1.)
        string = "("+str(i)+", "+str(j)+")"
        plt.scatter([xcoord],[ycoord],color='c',s=300)
        plt.annotate(string,xy=(xcoord+0.1,ycoord+0.1),color='c')
        print i, j, xcoord, ycoord

#for i in range(xminmap,xmaxmap+1):
#    plt.plot([xminmap,xmaxmap],[i,i],color='k')
#    plt.plot([i,i],[yminmap,ymaxmap],color='k')

plt.savefig('fakeSPH_grid')
    
plt.show()
