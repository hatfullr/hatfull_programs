"""
Author: Roger Hatfull
Institution: University of Alberta
Date: 01/16/2018
Version 2.0.3


** Description:
   This program is used to read binary data output from StarSmasher simulations for use in Python scripts.

   This function will need to be updated every time a change is made to how the output files are written.
   See output.f, subroutine 'dump', and starsmasher.h for more information. Also, for reading extra stuff
   from the files, check the formatting for the struct module: 
   https://docs.python.org/2/library/struct.htmlformat-characters

    
** Instructions:
   Place this file in your working directory and then import it using 'import read_sph_data as rsd'.
   Use the read function as 'rsd.read(datafile)'. See the examples below for help.


** Inputs:
   fmt_header       Specify a custom header format. Should be in the form of 'i3d2i' etc.
                    where 'i' is a 4-byte integer, '3d' is 3 8-byte doubles, and '2i' is 2 4-byte integers.
                    The leading junk and trailing endline are removed by default.

   fmt_dataline     Specify a custom format for each line of data after the header. Should be in the form
                    'f8,f8,f8,f8,f8,f4,f8,' etc. where 'f8' is an 8-byte double and 'f4' is a 4-byte float
                    (integer). The leading junk and trailing endline are removed by default.

   fmt_extra        Specify a custom format for any extra lines of data at the end of the data lines. This
                    is a simpler alternative to defining your own fmt_dataline.

   size_header      Give the size (bytes) of the header. The leading junk and trailing endline are removed
                    by default.

   size_dataline    Give the size (bytes) of each line of data. The trailing endline is removed by default.

   size_extra       Give the size (bytes) of your specified fmt_extra.


** Example:
   import read_sph_data as rsd
   datafile = 'out0000.sph'

   data = rsd.read(datafile) #Read an output file
   data, header = rsd.read(datafile,return_header=True) #Get data and header
   data = rsd.read(datafile,extra=8,extra_fmt='f8')     #Read one extra 64-bit double on each line
   data = rsd.read(datafile,extra=4,extra_fmt='i4')     #Read one extra 32-bit integer on each line
   data = rsd.read(datafile,extra=8,extra_fmt='f8, f8') #Read two extra 64-bit doubles on each line


** Troubleshooting:
   1) Try running your python script again after a few seconds. If you are reading in a file as it's
      being written, you will get an error.
   2) Numpy typically releases a warning regarding structured arrays assignment. You can either ignore this
      or turn it off by using:

      import warnings
      warnings.filterwarnings('ignore')

      at the top of your code.
   3) Make sure the formats for your header and datalines are correct. If your simulation has
      ncooling =/= 0, you may need to define your own format (check the format section below). If you
      have defined your own formats, compare your formats to the code's write step in the 'dump' subroutine
      in output.f. For your dataline format, try placing commas in different orders. Perhaps try removing
      only the leading comma, or only the trailing comma, or try removing both.
   4) Make sure the output file isn't corrupted. StarSmasher prints the total # of particles at the
      beginning and the end of each file to check for corruption.


** Formats:
   The following presented formats have the StarSmasher variable names listed separated by commas with their
   associated column number above them for quick reference.

   Each file has a header. At the time of publishing this code, this format follows,
   
   Headers:
      0     1     2     3      4     5    6     7     8   9  10    11     12       13      14     15
    ntot, nnopt, hco, hfloor, sep0, tf, dtout, nout, nit, t, nav, alpha, beta, tjumpahead, ngr, nrelax

      16    17    18       19      20      21         22         23         24
    trelax, dt, omega2, ncooling, erad, ndisplace, displacex, displacey, displacez

   After the header line, each file contains lines of data equal to the total number of particles 'ntot' in 
   the simulation. Each dataline has the format,

   Datalines:
      0  1  2  3   4    5   6   7   8     9     10     11   12   13    14         15        16   17   
      x, y, z, am, hp, rho, vx, vy, vz, vxdot, vydot, vzdot, u, udot, grpot, meanmolecular, cc, divv

     (18)*     (19)*
     (ueq)*, (tthermal)*

 * ncooling =/= 0. BY DEFAULT, read_sph_data DETECTS IF ncooling =/= 0 AND ADJUSTS THE DATALINE AUTOMATICALLY!


** Changes:
   2.0.4
      - Improved how read errors are reported.
   2.0.3
      - Moved the def statement to below this comment block.
      - Reformatted the comment block and made some edits.
   2.0.2
      - Now you can specify a custom header format and custom data format using fmt_header and fmt_dataline.

   2.0.1
      - Added compatibility for dynamical runs that have ncooling turned on.
   2.0.0
      - Basically completely revamped the program. It now runs ~100x faster, and I don't think it can be
        significantly optimized any further.
      - Only returns numpy arrays, for both the header and data. Thus, "asnparray" option is deprecated.
"""


def read(filename,
         return_header=False,
         return_data=True,
         fmt_header= '2i'+    # ntot, nnopt (2*4=8)
                     '5d'+    # hco, hfloor, sep0, tf, dtout (8*5=40)
                     '2i'+    # nout, nit (2*4=8)
                     'd'+     # t (8)
                     'i'+     # nav (4)
                     '3d'+    # alpha, beta, tjumpahead (3*8=24)
                     '2i'+    # ngr, nrelax (4*2=8)
                     '3d'+    # trelax, dt, omega2 (3*8=24)
                     'i'+     # ncooling (4)
                     'd'+     # erad (8)
                     'i'+     # ndisplace (4)
                     '3d',    # displacex, displacey, displacez (4*8=24),
         fmt_dataline= 'f8,'+ # x
                       'f8,'+ # y
                       'f8,'+ # z
                       'f8,'+ # am
                       'f8,'+ # hp
                       'f8,'+ # rho
                       'f8,'+ # vx
                       'f8,'+ # vy
                       'f8,'+ # vz
                       'f8,'+ # vxdot
                       'f8,'+ # vydot
                       'f8,'+ # vzdot
                       'f8,'+ # u
                       'f8,'+ # udot
                       'f8,'+ # grpot
                       'f8,'+ # meanmolecular
                       'f4,'+ # cc
                       'f8',  # divv
         fmt_extra='',
         size_header=164,
         size_dataline=156,
         size_extra=0,
         lines=0):
    import struct
    import numpy as np
    import sys
    from numpy.lib.recfunctions import repack_fields

    if fmt_extra != '': fmt_extra = ','+fmt_extra
    dsize = size_dataline+size_extra+8
    
    with open(filename,'rb') as f:
        header = np.asarray(struct.unpack('<i'+fmt_header+'d', f.read(4+size_header+8)))[1:-1]
        if lines == 0: lines = int(header[0])

        if int(header[19]) != 0: #if ncooling =/= 0
            fmt_dataline += ',f8,f8'
            dsize+=16

        if return_data:
            dtype = fmt_dataline+fmt_extra+',f8'
            data = np.zeros((lines,dtype.count(',')+1))
            try:
                #data = np.ndarray(shape=(1,lines),
                #                  dtype=np.dtype(fmt_dataline+fmt_extra+',f8'),
                #                  buffer=f.read(lines*dsize))[0].astype(dsize*'f8,').view(dtype='f8').reshape(lines,dsize)[:,:-1]
                
                data[:] = np.ndarray(shape=(1,lines),
                                     dtype=np.dtype(dtype),
                                     buffer=f.read(lines*dsize))[0].tolist()[:]
            except:
                print("read_sph_data.py: Failed to read '"+filename+"'. Make sure your fmt_dataline is correct. Open read_sph_data.py for more help.")
                raise
            
            data=data[:,:-1]
            
            if return_header: return data,header
            else: return data
        else:
            if return_header: return header
