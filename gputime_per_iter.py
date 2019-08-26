import numpy as np
import matplotlib.pyplot as plt

plt.style.use('supermongo')

data = np.loadtxt("gputime_per_iter.dat")

t = data[:,0]
gputime = data[:,1]

array = np.vstack((t,gputime)).T

array = array[array[:,0].argsort()]

t = array[:,0]
gputime = array[:,1]

cumgputime = np.cumsum(gputime)



fig, ax = plt.subplots(2,sharex=True)


ax[0].scatter(t,gputime,color='k',s=1)
ax[0].set_ylabel("GPU time per iteration [sec]")
ax[0].set_ylim(bottom=0.)

ax[1].plot(t,cumgputime/60./60.,color='k')
ax[1].set_xlabel("Time [code units]")
ax[1].set_ylabel("Cumulative GPU time [hours]")

plt.savefig("gputime_per_iter.eps")
plt.savefig("gputime_per_iter.png")
plt.show()
