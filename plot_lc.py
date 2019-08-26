import numpy as np
import matplotlib.pyplot as plt
import sys
import matplotlib as mpl
import glob

# Setup the matplotlib rcParams
mpl.rcParams['lines.linewidth'] = 1
mpl.rcParams['font.family'] = 'monospace'
mpl.rcParams['font.weight'] = 300
mpl.rcParams['font.size'] = 12.0
mpl.rcParams['font.monospace'] = 'DejaVu Sans'
mpl.rcParams['mathtext.default'] = 'regular'

#mpl.rcParams['text.color'] = 'white'
#mpl.rcParams['axes.facecolor'] = 'black'
#mpl.rcParams['axes.edgecolor'] = 'white'
#mpl.rcParams['axes.labelcolor'] = 'white'

mpl.rcParams['xtick.top'] = True
mpl.rcParams['xtick.major.size'] = 9
mpl.rcParams['xtick.minor.size'] = 4
mpl.rcParams['xtick.major.width'] = 0.5
mpl.rcParams['xtick.minor.width'] = 0.5
#mpl.rcParams['xtick.color'] = 'white'
mpl.rcParams['xtick.labelsize'] = 'medium'
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['xtick.minor.visible'] = True

mpl.rcParams['ytick.right'] = True
mpl.rcParams['ytick.major.size'] = 9
mpl.rcParams['ytick.minor.size'] = 4
mpl.rcParams['ytick.major.width'] = 0.5
mpl.rcParams['ytick.minor.width'] = 0.5
#mpl.rcParams['ytick.color'] = 'white'
mpl.rcParams['ytick.labelsize'] = 'medium'
mpl.rcParams['ytick.direction'] = 'in'
mpl.rcParams['ytick.minor.visible'] = True

mpl.rcParams['figure.titleweight'] = 300
mpl.rcParams['figure.figsize'] = (8.0, 8.0)
mpl.rcParams['figure.subplot.right'] = 0.85
mpl.rcParams['figure.subplot.bottom'] = 0.10
mpl.rcParams['figure.subplot.top'] = 0.95


def read_file(filename):

    # Figure out the shape of the data
    with open(filename,'r') as f:
        for i in range(0,5):
            f.readline()
        shape1 = 0
        for line in f:
            shape1 += 1
        line = filter(lambda a: a != '',line.split(" "))
        shape2 = len(line)


    data = np.zeros((shape1,shape2))
    with open(filename,'r') as f:
        for i in range(0,5):
            f.readline()
        linenum = 0
        for line in f:
            line = filter(lambda a: a != '',line.split(" "))
            line[-1] = line[-1][:-1]

            dataline = np.array([])
            
            data[linenum][0] = float(line[0][8:12])
            for i in range(1,len(line)):
                data[linenum][i] = float(line[i])
            linenum += 1
    return data

user_input = raw_input("Enter file name(s) or patterns: ").split(" ")

files = []
for pattern in user_input:
    for i in sorted(glob.glob(pattern)):
        files.append(i)

filenum = np.array([])
L = np.array([])
for filename in files:
    data = read_file(filename)
    filenum = np.append(filenum,data[:,0])
    L = np.append(L,data[:,1])
    

#time = time * np.sqrt(runit**3./Gunit/munit) * days * 0.5

plt.plot(filenum,L,color='k',label="$L_{\\mathrm{tot}}$")

plt.xlabel("File number")
plt.ylabel("$L$")
plt.tight_layout()

print "Maximum luminosity =",max(L)
print "Occurs at file number",filenum[np.where(max(L)==L)[0][0]]

plt.savefig("light_curve.png")
plt.show()
