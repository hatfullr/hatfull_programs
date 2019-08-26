import matplotlib.pyplot as plt
import numpy as np

plt.style.use('supermongo')

gravconst = 6.67390e-08
runit = 6.9599e10
munit = 1.9891e33

data = np.loadtxt("energy0.sph")
t = data[:,0]*np.sqrt(runit**3. / (gravconst*munit))/60./60./24.
eint = data[:,3]*gravconst*munit/runit / 1.e15
epot = data[:,1]*gravconst*munit/runit / 1.e15
ekin = data[:,2]*gravconst*munit/runit / 1.e13
etot = data[:,4]*gravconst*munit/runit / 1.e14

fig, ax = plt.subplots(nrows=4,ncols=1,sharex=True)


ax[0].plot(t,eint,color='k')
ax[1].plot(t,epot,color='k')
ax[2].plot(t,ekin,color='k')
ax[3].plot(t,etot,color='k')



ax[0].set_ylabel("$U\\ \\left[10^{15}\\ \\mathrm{ergs}\\right]$")
ax[1].set_ylabel("$W\\ \\left[10^{15}\\ \\mathrm{ergs}\\right]$")
ax[2].set_ylabel("$T\\ \\left[10^{13}\\ \\mathrm{ergs}\\right]$")
ax[3].set_ylabel("$E\\ \\left[10^{14}\\ \\mathrm{ergs}\\right]$")
ax[3].set_xlabel("Time$\\ \\left[\\mathrm{days}\\right]$")

for i in ax:
    i.get_yaxis().set_label_coords(-0.1,0.5)


plt.subplots_adjust(bottom=0.1)

plt.savefig("v0.eps")
plt.savefig("v0.png")

plt.show()
