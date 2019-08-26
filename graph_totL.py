import numpy as np
import matplotlib.pyplot as plt
import os
import glob
import matplotlib.transforms as mtransforms

#cur_dir = os.getcwd()
cur_dir = "/home/hatfull/data/ulfhednar/dynamical/d003u_b002u_1.195M_0.32M_40k_1_1.2G0.32C0.32D_ncooling1/lc_splot136_rotating_rossonly/"
opacityfile = glob.glob(cur_dir+"sph.opacit*")[0].split("/")[-1]
lcfile = cur_dir+"lc_70deg"

a = np.float64(7.5657e-15) #erg/cm^3/K^4
k = np.float64(1.38064852e-16) #erg/K
m_H = np.float64(1.6737236e-24) #g
g = np.float64(1./1000.) #kg
cm = np.float64(1./100.) #m
s = np.float64(1.)
J = np.float64(g * cm**2. / s**2.) #Joules
G = np.float64(1./(6.67408e-11 / cm**3. * g * s**2.)) #Gravitational cosntant in cgs
Ms = np.float64(1./(1.9891e30 / g)) #Mass of the sun in cgs
Rs = np.float64(1./(6.9599e8 / cm)) #Radius of the sun in cgs
Ls = np.float64(1./3.839e33) #Luminosity of the sun in cgs
gamma = 5./3.
codetime = np.float64(1./np.sqrt(G * Ms / Rs**3.)) # seconds
days = np.float64(1./ (codetime * 60 * 60 * 24))


fig, (ax1, ax2) = plt.subplots(2,1,sharex='none',figsize=(8,8))

data = np.genfromtxt(lcfile)

date = data[:,0]#*24*60*60 / np.sqrt(G * Ms / Rs**3.) #in code units
totL = data[:,1]

ax1.plot(date, totL/Ls/(10**37),color='k',marker='.')
#ax1.axvspan(5500*days, 6500*days, color='b',alpha=0.25,label="Plunge-in")
ax1.set_ylabel("Total \"Luminosity\" [10$^{37}$ ergs s$^{-1}$]")
ax1.set_xlabel("time [days]")


ax2.plot(date,np.log10(totL/Ls),color='k',marker='.')
#ax2.axvspan(5500*days, 6500*days, color='b',alpha=0.25,label="Plunge-in")
ax2.set_xlabel("time [days]")
ax2.set_ylabel("log$_{10}$ Total \"Luminosity\" [ergs s$^{-1}$]")

plt.suptitle(cur_dir.split("/")[-3])
ax1.set_title(opacityfile,loc='left')
ax1.set_title("_".join(cur_dir.split("/")[-2].split("_")[1:]),loc='right')
    
plt.tight_layout()
fig.subplots_adjust(top=0.92)
plt.savefig(cur_dir.split("/")[-3].split("_")[0]+"_"+"_".join(cur_dir.split("/")[-2].split("_")[1:])+"_totL.png")

plt.show()

