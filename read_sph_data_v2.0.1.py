def read(filename,extra=0,extra_fmt='',return_header=False,asnparray=True):
    #Author: Roger Hatfull
    #Institution: University of Alberta
    #Date: 07/06/2017
    #Version 2.0.1

    #This is used to read in binary data output from StarSmasher simulations.
    #Place it in your working directory and then import it using
    #'import read_sph_data as rsd'
    
    #This function will need to be updated every time a change is made to how the output
    #files are written. See output.f, subroutine 'dump', and starsmasher.h for more
    #information. Also, for reading extra stuff from the files, check the formatting for
    #the struct module: https://docs.python.org/2/library/struct.html#format-characters
    
    #Usage Examples:
    #    import read_sph_data as rsd
    #    datafile = 'out0000.sph'
    #
    #    data = rsd.read(datafile) #Read an output file
    #    data, header = rsd.read(datafile,return_header=True) #Get data and header
    #    data = rsd.read(datafile,extra=8,extra_fmt='f8')     #Read one extra 64-bit double on each line
    #    data = rsd.read(datafile,extra=4,extra_fmt='i4')     #Read one extra 32-bit integer on each line
    #    data = rsd.read(datafile,extra=8,extra_fmt='f8, f8') #Read two extra 64-bit doubles on each line

    #Output file header format:
    #   0     1     2     3      4     5    6     7     8   9  10    11     12       13      14     15
    # ntot, nnopt, hco, hfloor, sep0, tf, dtout, nout, nit, t, nav, alpha, beta, tjumpahead, ngr, nrelax
    #
    #   16    17    18       19      20      21         22         23         24
    # trelax, dt, omega2, ncooling, erad, ndisplace, displacex, displacey, displacez
    
    #Output file meat format:
    # 0  1  2  3   4    5   6   7   8     9     10     11   12   13    14         15        16   17   (18)*     (19)*
    # x, y, z, am, hp, rho, vx, vy, vz, vxdot, vydot, vzdot, u, udot, grpot, meanmolecular, cc, divv, (ueq)*, (tthermal)*
    #
    # * ncooling =/= 0

    #Changes:
    #   2.0.1
    #      - Added compatibility for dynamical runs that have ncooling turned on.
    #
    #   2.0.0
    #      - Basically completely revamped the program. It now runs ~100x faster, and I don't think it can be
    #        significantly optimized any further.
    #      - Only returns numpy arrays, for both the header and data. Thus, "asnparray" option is deprecated.
    
    import struct
    import numpy as np
    
    with open(filename,'rb') as f:
        header = np.asarray(struct.unpack('<i'+ #junk (4)
                                          '2i'+ #ntot, nnopt (2*4=8)
                                          '5d'+ #hco, hfloor, sep0, tf, dtout (8*5=40)
                                          '2i'+ #nout, nit (2*4=8)
                                          'd'+ #t (8)
                                          'i'+ #nav (4)
                                          '3d'+ #alpha, beta, tjumpahead (3*8=24)
                                          '2i'+ #ngr, nrelax (4*2=8)
                                          '3d'+ #trelax, dt, omega2 (3*8=24)
                                          'i'+ #ncooling (4)
                                          'd'+ #erad (8)
                                          'i'+ #ndisplace (4)
                                          '3d'+ #displacex, displacey, displacez (4*8=24)
                                          'd', #junk (8)
                                          f.read(176)))[1:-1]
        lines = int(header[0])
        if extra_fmt != '': extra_fmt = extra_fmt+','
        if header[19] == 0:
            data = np.ndarray(shape=(1,lines),
                              dtype=np.dtype(16*'f8,'+'f4,'+'f8,'+extra_fmt+'f8'),
                              buffer=f.read(lines*(16*8+4+8+extra+8)))[0].astype(20*'f8,').view(dtype='f8').reshape(lines,20)[:,:-1]
        else:
            data = np.ndarray(shape=(1,lines),
                              dtype=np.dtype(16*'f8,'+'f4,'+3*'f8,'+extra_fmt+'f8'),
                              buffer=f.read(lines*(16*8+4+3*8+extra+8)))[0].astype(22*'f8,').view(dtype='f8').reshape(lines,22)[:,:-1]

    if return_header: return data,header
    else: return data
