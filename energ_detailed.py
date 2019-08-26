import matplotlib.pyplot as plt
import numpy as np
import os

plt.style.use('supermongo')

data = np.loadtxt("energy_comparison.dat")


m = data[:,0]
eri = data[:,5]
erp = data[:,8]
etsph = data[:,9]
etmesa = data[:,10]
ert = data[:,11]
eris = data[:,14]
erps = data[:,17]
serr = data[:,20]


# Look at the top 10% of the mass for the surface
mmax = m[0]
mmin = m[np.where(m >= 0.9*mmax)][-1]


#figsize is height & width in inches. Standard .eps file from energ_detailed.sm is 202 x 202 mm = 8 x 8 in.
fig, ax = plt.subplots(3,sharex=True,figsize=(8,8))


#Specific energies error
ax[0].plot(m,eris,color='b',linewidth=1,label='specific int')
ax[0].plot(m,erps,color='r',linewidth=1,label='specific pot')
ax[0].plot(m,serr,color='k',linewidth=1,label='entropy error')
ax[0].set_xlim(mmin, mmax)
ax[0].set_ylim(-0.1,0.1)
ax[0].set_ylabel("$\\delta$ error, rel.fr.")
ax[0].annotate('entropy error',color='k',xy=(0.5,0.6),xycoords='axes fraction')
ax[0].annotate('specific int',color='b',xy=(0.5,0.7),xycoords='axes fraction')
ax[0].annotate('specific pot',color='r',xy=(0.5,0.8),xycoords='axes fraction')



#Integrated energies error
ax[1].plot(m,eri,color='b',linewidth=1,label='integrated int')
ax[1].plot(m,erp,color='r',linewidth=1,label='integrated pot')
ax[1].plot(m,ert, color='k',linewidth=1, label='total')
ax[1].set_ylabel("$\\delta$ error, rel.fr.")
ax[1].set_xlim(mmin,mmax)
ax[1].set_ylim(-0.1,0.1)
ax[1].annotate('total',color='k',xy=(0.5,0.6),xycoords='axes fraction')
ax[1].annotate('integrated int',color='b',xy=(0.5,0.7),xycoords='axes fraction')
ax[1].annotate('integrated pot',color='r',xy=(0.5,0.8),xycoords='axes fraction')


#Integrated energies difference between MESA and SPH
ax[2].plot(m,((etmesa-etsph)*1.e4),color='k',linewidth=1,label='$\\int E_{\\mathrm{tot, Mesa}} -$\n$\\int E_{\\mathrm{tot,SPH}}$')
ax[2].set_xlabel('mass')
ax[2].set_ylabel("$E/10^{44}$ erg")
ax[2].set_xlim(mmin,mmax)
ax[2].set_ylim(-10,10)
ax[2].annotate('integrated EtotMesa - EtotSPH',color='k',xy=(0.5,0.8),xycoords='axes fraction')


ax[0].set_title(os.path.basename(os.getcwd()))
plt.tight_layout()
plt.subplots_adjust(wspace=0, hspace=0)


        
plt.savefig("energy_detailed_py.png")

        
