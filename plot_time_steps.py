import numpy as np
import matplotlib.pyplot as plt

# Before using this code, run get_time_steps:
##!/bin/bash
#if [ -f $1 ]; then
#    grep "tstep: dts= " $1 | awk  '{print $3,$4,$5,$6,$7}' > timesteps.dat
#else
#    echo "ERROR: Could not find file $1."
#fi

plt.style.use('supermongo')

data = np.loadtxt("timesteps.dat")


dtvelmin = data[:,0]
dtaccmin = data[:,1]
dtumin = data[:,2]
dtacc4min = data[:,3]
dt = data[:,4]

t = np.cumsum(dt)
x = np.arange(len(dt))

plt.scatter(t,dt,color='k',s=1)

plt.xlabel("Time [code units]")
plt.ylabel("Time Stepsizes [code units]")

plt.tight_layout()
plt.savefig("timesteps.eps")
plt.savefig("timesteps.png")
plt.show()
