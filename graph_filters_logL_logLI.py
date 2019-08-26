import numpy as np
import matplotlib.pyplot as plt
import os
import glob
from matplotlib.ticker import LogLocator, AutoLocator
from cycler import cycler
import matplotlib as mpl

mpl.rcParams['axes.prop_cycle'] = cycler('color',['#1f77b4',
                                                  '#ff7f0e',
                                                  '#2ca02c',
                                                  '#d62728',
                                                  '#9467bd',
                                                  '#8c564b',
                                                  '#e337c2',
                                                  '#7f7f7f',
                                                  '#bcbd22',
                                                  '#17becf'])

cur_dir = "/home/hatfull/data/graham/dynamical/d007g_b009g_1.52M_0.142598M_50k_1_v1309/lc_splot136_rotating_rossonly/"
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


data = np.genfromtxt(lcfile)

date = data[:,0]#*24*60*60 / np.sqrt(G * Ms / Rs**3.) #in code units

distance = 3500 #parsecs

for i in range(55,64): data[:,i] = data[:,i]+5*np.log10(distance/10)

#Extinction is A_lambda / A_v. A_v for an E(B-V)=0.8 (Tylenda et al. 2011) is A_v = 2.47.
#A_lambda/A_v values are found from the CTIO/UKIRT filters which are similar to the OGLE-III and
#OGLE-IV filters, in Cardelli, Clayton & Mathis (1989). The formula for the extinction is then
#m_lambda = m_lambda,o + A_lambda
#where m_lambda,o is the magnitude without extinction.

# Filter   A_lambda/A_v
#   U         1.521
#   B         1.324
#   V         0.992
#   R         0.807
#   I         0.601
#   J         0.276
#   H         0.176
#   K         0.112
#   L         0.047

A_v = 2.47

U = data[:,55] + 1.521 * A_v
B = data[:,56] + 1.324 * A_v
V = data[:,57] + 0.992 * A_v
R = data[:,58] + 0.807 * A_v
I = data[:,59] + 0.601 * A_v
J = data[:,60] + 0.276 * A_v
H = data[:,61] + 0.176 * A_v
K = data[:,62] + 0.112 * A_v
L = data[:,63] + 0.047 * A_v

I2 = data[:,59]
totL = np.log10(data[:,1])
#The number 2.416e-20 comes from optical_depth.f
L_I = np.log10(4 * np.pi * distance**2. * 2.416e-20 * 10**(-2./5. * I2))

fig, (ax1, ax2) = plt.subplots(2,1,sharex=True,figsize=(8,8))

ax1.set_ylabel("apparent magnitude")
ax1.set_title(opacityfile,loc='left')
ax1.set_title("_".join(cur_dir.split("/")[-2].split("_")[1:]),loc='right')
ax2.set_xlabel("time [days]")
ax2.set_ylabel("log$_{10}$ $L/L_{\\rm{odot}}$")

ax1.tick_params(axis='both',which='both',direction='in',top=True,bottom=True,left=True,right=True)
ax2.tick_params(axis='both',which='both',direction='in',top=True,bottom=True,left=True,right=True)

plt.suptitle(cur_dir.split("/")[-3]+"         distance=3500pc")

plots = np.array([])

plots = np.append(plots,ax1.plot(date,U,label="U"))
plots = np.append(plots,ax1.plot(date,B,label="B"))
plots = np.append(plots,ax1.plot(date,V,label="V"))
plots = np.append(plots,ax1.plot(date,R,label="R"))
plots = np.append(plots,ax1.plot(date,I,label="I"))
plots = np.append(plots,ax1.plot(date,J,label="J"))
plots = np.append(plots,ax1.plot(date,H,label="H"))
plots = np.append(plots,ax1.plot(date,K,label="K"))
plots = np.append(plots,ax1.plot(date,L,label="L"))

plots = np.append(plots,ax2.plot(date,totL,label="$L_{\\rm{tot}}$",color='k'))
plots = np.append(plots,ax2.plot(date,L_I,label="$L_I$",color='r'))

alldata = np.array([])
alldata = np.append(alldata,U)
alldata = np.append(alldata,B)
alldata = np.append(alldata,V)
alldata = np.append(alldata,R)
alldata = np.append(alldata,I)
alldata = np.append(alldata,J)
alldata = np.append(alldata,K)
alldata = np.append(alldata,H)
alldata = np.append(alldata,L)

alldatalog = np.append(totL, L_I)

delx = max(date) - min(date)
dely = max(alldata) - min(alldata)
delylog = max(alldatalog) - min(alldatalog)

xlim = [min(date) - delx*0.05,max(date) + delx*0.05]
ylim = [min(alldata) - dely*0.05,max(alldata) + dely*0.05]
ylimlog = [min(alldatalog) - delylog*0.05, max(alldatalog) + delylog*0.05]

ax1.set_xlim(xlim)
ax1.set_ylim(ylim)
ax2.set_xlim(xlim)
ax2.set_ylim(ylimlog)

ax1.invert_yaxis()

legend = plt.legend(plots,["U","B","V","R","I","J","H","K","L","$L_{\\rm{tot}}$","$L_I$"],
                    bbox_to_anchor=(0., -0.25, 1., .102), loc=0,
                    ncol=11, mode="expand", borderaxespad=0.,prop={'size': 12})


plt.tight_layout()
fig.subplots_adjust(top=0.92,bottom=0.1,hspace=0)

plt.savefig(cur_dir.split("/")[-3].split("_")[0]+"_"+"_".join(cur_dir.split("/")[-2].split("_")[1:])+"_filters_logL_logLI.png")

plt.show()
