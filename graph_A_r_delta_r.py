import numpy as np
import glob
import read_sph_data as rsd
import warnings
import matplotlib.pyplot as plt
import matplotlib as mpl

plt.rcParams['axes.facecolor'] = 'grey'

warnings.filterwarnings('ignore')

simdir = "/home/hatfull/data/graham/relax/r050g_1.52M_2350Myr_100k_WC4_69_nnopt_1.4x_hp1/"
datafiles = sorted(glob.glob(simdir+"col*.sph"))
parentfile = simdir+"parent.sph"
moddir = "/home/hatfull/data/ulfhednar/starsev/s001u_V1309/models/"
modelfile = moddir+"m_1.52_t_2350.mod.muse"

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
gamma = 5./3.


def read_data(datafile):
    data_code = np.loadtxt(datafile)
    
    t_code = int(datafile.split("/")[-1][3:7])

    r_code = data_code[:,0]
    P_code = data_code[:,1]
    rho_code = data_code[:,2]

    r_code = r_code[np.where(P_code > 0)]
    rho_code = rho_code[np.where(P_code > 0)]
    P_code = P_code[np.where(P_code > 0)]
    
    A_code = P_code / (rho_code**(5./3.))
    
    return t_code, r_code, A_code

def read_parent():
    data_parent = np.loadtxt(parentfile)

    r_parent = data_parent[:,0]
    P_parent = data_parent[:,1] #/ Ms * Rs * s**2.
    rho_parent = data_parent[:,2] #/ Ms * Rs**3.

    A_parent = P_parent / (rho_parent**(5./3.))

    return r_parent, A_parent

r_parent, A_parent = read_parent()

t_code1, r_code1, A_code1 = read_data(min(datafiles))
t_code2, r_code2, A_code2 = read_data(max(datafiles))

#delta_A = abs(A_code2 - A_code1)
delta_r = r_code2 - r_code1

maxdelr = np.where(delta_r > max(delta_r)*0.6)
#maxdelA = np.where(delta_A > max(delta_A)*0.6)


if -min(delta_r) > max(delta_r):
    vmin = min(delta_r)
    vmax = -vmin
else:
    vmax = max(delta_r)
    vmin = -vmax

plt.plot(r_parent, np.log10(A_parent), color='k')
    
cm = plt.cm.get_cmap('bwr')
sc = plt.scatter(r_code2, np.log10(A_code2),
                 marker='.',
                 s=1,
                 edgecolors='none',
                 c=delta_r,
                 cmap=cm,
                 vmin=vmin,
                 vmax=vmax)
cbar = plt.colorbar(sc)
cbar.ax.set_ylabel('$r_{\\rm{final}}-r_{\\rm{initial}}$')

plt.xlim(min(r_code2)*0.9,max(r_code2)*1.1)
plt.ylim(min(np.log10(A_code2))*0.9, max(np.log10(A_code2))*1.1)
plt.xlabel("$r$")
plt.ylabel("$A$")
plt.title(simdir.split("/")[-2]).set_position([0.5,1.05])
plt.tight_layout()
plt.savefig(simdir.split("/")[-2].split("_")[0]+"_A_r_delta_r.png")

plt.show()

