import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.cm as cm
import matplotlib.colors as cols
import glob
import sys
import matplotlib as mpl

# Setup the matplotlib rcParams
mpl.rcParams['lines.linewidth'] = 1
mpl.rcParams['font.family'] = 'monospace'
mpl.rcParams['font.weight'] = 300
mpl.rcParams['font.size'] = 12.0
mpl.rcParams['font.monospace'] = 'DejaVu Sans'
mpl.rcParams['mathtext.default'] = 'regular'

mpl.rcParams['text.color'] = 'white'
mpl.rcParams['axes.facecolor'] = 'black'
mpl.rcParams['axes.edgecolor'] = 'white'
mpl.rcParams['axes.labelcolor'] = 'white'

mpl.rcParams['xtick.top'] = True
mpl.rcParams['xtick.major.size'] = 9
mpl.rcParams['xtick.minor.size'] = 4
mpl.rcParams['xtick.major.width'] = 0.5
mpl.rcParams['xtick.minor.width'] = 0.5
mpl.rcParams['xtick.color'] = 'white'
mpl.rcParams['xtick.labelsize'] = 'medium'
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['xtick.minor.visible'] = True

mpl.rcParams['ytick.right'] = True
mpl.rcParams['ytick.major.size'] = 9
mpl.rcParams['ytick.minor.size'] = 4
mpl.rcParams['ytick.major.width'] = 0.5
mpl.rcParams['ytick.minor.width'] = 0.5
mpl.rcParams['ytick.color'] = 'white'
mpl.rcParams['ytick.labelsize'] = 'medium'
mpl.rcParams['ytick.direction'] = 'in'
mpl.rcParams['ytick.minor.visible'] = True

mpl.rcParams['figure.titleweight'] = 300
mpl.rcParams['figure.figsize'] = (8.0, 8.0)
mpl.rcParams['figure.subplot.right'] = 0.85
mpl.rcParams['figure.subplot.bottom'] = 0.10
mpl.rcParams['figure.subplot.top'] = 0.95

mpl.rcParams['figure.facecolor'] = 'black'
mpl.rcParams['figure.edgecolor'] = 'black'

titleheight=0.878
titleoffset=0.205

user_input = raw_input("Enter file name(s) or patterns: ").split(" ")
files = []
for pattern in user_input:
    for i in sorted(glob.glob(pattern)):
        if ((i[:6] != "fluxes") or (i[-4:] != ".sph")):
            print "ERROR: You must provide fluxes files from flux_cal output."
            print "Error on file",i
            sys.exit()
        files.append(i)

user_input = raw_input("Use adaptive plot limits? (y/n): ")
if user_input == "y":
    adaptivelimits = True
elif user_input == "n":
    adaptivelimits = False
else:
    "ERROR: Please respond with 'y' or 'n'."
    sys.exit()

        
# Create the plot

fig = plt.figure()
ax = plt.gca()
        
# Create the colorbar
    
vmin = 0.
vmax = 10000.
norm = cols.Normalize(vmin,vmax)

mlibcolorbar=False
try:
    print "Getting live website data for blackbody spectrum colors..."
    import urllib2
    website = 'http://www.vendian.org/mncharity/dir3/blackbody/UnstableURLs/bbr_color.html'
    
    page = urllib2.urlopen(website)
    for i in range(0,20): page.readline() # Skip the header
    
    content = page.readlines()[1:-4][::2]
    content = np.asarray(content)
    
    #content = np.delete(content,0,axis=0)
    bbcols = np.zeros((len(content),4))
    for i in range(0,len(content)):
        content[i] = content[i][34:-17]
        bbcols[i][0] = float(content[i][:5])
        bbcols[i][1] = float(content[i][44:50])
        bbcols[i][2] = float(content[i][51:57])
        bbcols[i][3] = float(content[i][58:64])
        
    Nbbcols = len(bbcols)
    colors = np.reshape(bbcols[:,1:],(Nbbcols,3))
    colors = colors[np.where((bbcols[:,0] > vmin) & (bbcols[:,0] < vmax))[0]]
    my_cm = cols.LinearSegmentedColormap.from_list(
        'blackbody', colors, N=Nbbcols)
    print "SUCCESS"
except:
    print "FAILED"
    try:
        print ""
        print "Getting blackbody spectrum colors from blackbody_temps.dat in the working directory..."
        bbcols = np.genfromtxt("blackbody_temps.dat",usecols=(0,6,7,8))
        Nbbcols = len(bbcols)
        colors = np.reshape(bbcols[:,1:],(Nbbcols,3))
        colors = colors[np.where((bbcols[:,0] > vmin) & (bbcols[:,0] < vmax))[0]]
        my_cm = cols.LinearSegmentedColormap.from_list(
            'blackbody', colors, N=Nbbcols)
        print "SUCCESS"
    except:
        print "FAILED"
        print ""
        print "Using a standard matplotlib 'inferno' colorbar..."
        mlibcolorbar = True
        my_cm = plt.cm.get_cmap('inferno')
        print "SUCCESS"

im = plt.imshow([[0],[0]],cmap=my_cm)
divider = make_axes_locatable(ax)
cax = divider.append_axes('right',size='5%',pad=0.05)
cb = plt.colorbar(im,cax=cax)
plt.clim(vmin,vmax)

cbar_label = "$T_{\\mathrm{eff}}\\ \\left[K\\right]$"
cb.set_label(cbar_label)


if not adaptivelimits:
    # Read all the datafiles and find the maximum viewport
    xmaxx = -1e30
    ymaxx = -1e30
    xminn = 1e30
    yminn = 1e30
    for datafile in files:
        grid = np.genfromtxt(datafile,max_rows=1)
    
        xmin = grid[0]
        hxmap = grid[1]
        nx = int(grid[2])
        ymin = grid[3]
        hymap = grid[4]
        ny = int(grid[5])
        
        xmax = xmin + hxmap * nx
        ymax = ymin + hymap * ny

        if xmin < xminn: xminn = xmin
        if ymin < yminn: yminn = ymin
        if xmax > xmaxx: xmaxx = xmax
        if ymax > ymaxx: ymaxx = ymax


    dx = xmaxx - xminn
    dy = ymaxx - yminn
    if dx > dy:
        ymaxx = yminn + (dy+dx)/2.
        yminn = yminn + (dy-dx)/2.
        #ax.set_ylim(ymin + (dy-dx)/2., ymin + (dy+dx)/2.)
    elif dx < dy:
        xmaxx = xminn + (dx+dy)/2.
        xminn = xminn + (dx-dy)/2.
        #ax.set_xlim(xmin + (dx-dy)/2., xmin + (dx+dy)/2.)

for datafile in files:

    # Get the grid data

    grid = np.genfromtxt(datafile,max_rows=1)
    
    xmin = grid[0]
    hxmap = grid[1]
    nx = int(grid[2])
    ymin = grid[3]
    hymap = grid[4]
    ny = int(grid[5])
    
    xmax = xmin + hxmap * nx
    ymax = ymin + hymap * ny
    
    # Get the Teff data
    
    data = 10.**(np.genfromtxt(datafile,skip_header=1,max_rows=ny))
    
    data[np.isneginf(data)] = np.nan # Set all -inf to NaN
    data[np.where(data == 0.)] = np.nan # Set all T=0 to NaN

    if(mlibcolorbar):
        colors = np.array([])
        for i in range(0, ny):
            for j in range(0,nx):
                colors = np.append(colors, 10.**data[i][j])

    # Plot the data
    
    im = ax.imshow(np.flip(data,0),cmap=my_cm,vmin=vmin,vmax=vmax,
                    aspect='equal',extent=(xmin,xmax,ymin,ymax))

    if adaptivelimits:
    
        # Center and square the plotted region
    
        dx = ax.get_xlim()[1] - ax.get_xlim()[0]
        dy = ax.get_ylim()[1] - ax.get_ylim()[0]
        
        if dx > dy:
            ax.set_ylim(ymin + (dy-dx)/2., ymin + (dy+dx)/2.)
        elif dx < dy:
            ax.set_xlim(xmin + (dx-dy)/2., xmin + (dx+dy)/2.)

    else:
        ax.set_xlim(xminn,xmaxx)
        ax.set_ylim(yminn,ymaxx)

    # Re-plot the axis labels

    ax.set_xlabel("x")
    ax.set_ylabel("y")

    # Update the plot title
    
    rotations = datafile.split("/")[-1][12:-4].split("_")
    zdeg = int(rotations[0])
    ydeg = int(rotations[1])
    xdeg = int(rotations[2])
    ax.set_title("Rotations:\n")
    ax.annotate("x-axis=",(0+titleoffset,titleheight),xycoords='figure fraction',ha='left')
    ax.annotate(str(xdeg)+"$^o$",(0.128+titleoffset,titleheight),xycoords='figure fraction',ha='right')
    ax.annotate("y-axis=",(0.2+titleoffset,titleheight),xycoords='figure fraction',ha='left')
    ax.annotate(str(ydeg)+"$^o$",(0.328+titleoffset,titleheight),xycoords='figure fraction',ha='right')
    ax.annotate("z-axis=",(0.4+titleoffset,titleheight),xycoords='figure fraction',ha='left')
    ax.annotate(str(zdeg)+"$^o$",(0.528+titleoffset,titleheight),xycoords='figure fraction',ha='right')
        
    # Save the image

    print "Average Teff =", np.mean(data[~np.isnan(data)]), "K"
    
    savename = "Teffs"+datafile.split("/")[-1][6:-4]+".png"
    print "Saving", savename
    plt.savefig(savename,facecolor=fig.get_facecolor())

    # Clear the axis
    
    ax.clear()

print "Finished."
if len(files) > 1:
    print ""
    print "Use this command to make a movie:"
    print "convert -delay 10 -loop 0 Teffs*.png Teffs.gif"
    
