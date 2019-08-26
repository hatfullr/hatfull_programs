      program getFiltersFromFluxes
      implicit none
      
      character*255 fname
      logical fileexists

      integer nxmapmax,nymapmax
      parameter (nxmapmax=499,nymapmax=499)
      real*8 TpracticalXY(nxmapmax,nymapmax)
      integer nsl
      parameter(nsl=10)
      integer ilogwavelengthmin,ilogwavelengthmax
      parameter (ilogwavelengthmin=-150,ilogwavelengthmax=150)
      real*8 fluxdensity(ilogwavelengthmin:ilogwavelengthmax,0:nsl)
      integer numfiltersmax,numfilters
      parameter(numfiltersmax=15)
      real wavelength(numfiltersmax)

      real*8 xminmap,yminmap,hxmap,hymap
      integer nxmap,nymap

      character*2 filtername(numfiltersmax)

      real*8 fluxdensityXY(nxmapmax,nymapmax,numfiltersmax)

      real totalfluxdensity(numfiltersmax),absoluteflux(numfiltersmax)
      real mag(numfiltersmax)
      integer i,j
      integer ifilter
      integer dummy

      character*30 dummychar(10)
      character*2 dc2
      character*13 dc13
      character*26 dc26
      character*30 dc30
      character*34 dc34
      character*37 dc37

      integer start,finish,step
      real*8 anglex,angley,anglez

      integer innit

      character*255 outfile

      outfile="filter_mags.dat"
      
      write(*,*) "Enter start, finish, step:"
      read(*,*) start,finish,step

      write(*,*) "Enter rotation in z,y,x:"
      read(*,*) anglez,angley,anglex
      
 103  format ('fluxes',I5.5,'_',I3.3,'_',I3.3,'_',I3.3,'.sph')
 104  format ('fluxes',I6.6,'_',I3.3,'_',I3.3,'_',I3.3,'.sph')

      write(*,*) "Overwriting old output file '" //
     $     trim(adjustl(outfile)) // "'"
      open(60,file=trim(adjustl(outfile)),status='replace')      
      close(60)
      
      do innit=start,finish,step
         if(innit.le.99999) then
            write (fname,103) innit,nint(anglez),nint(angley),
     $           nint(anglex)
         else
            write(fname,104) innit,nint(anglez),nint(angley),
     $           nint(anglex)
         end if
         
c         write(*,*) "Reading file '" // trim(adjustl(fname)) // "'"
         inquire(file=trim(adjustl(fname)),exist=fileexists)
         
         if(.not.fileexists) then
            write(*,*) "Error reading file '" //
     $           trim(adjustl(fname)) // "'"
            error stop "File does not exist!"
         end if
         
         open (72,file=trim(adjustl(fname)))
         read(72,*)xminmap,hxmap,nxmap,yminmap,hymap,nymap
         
         do j=1,nymap
            read(72,'(2001f8.3)') (TpracticalXY(i,j),i=1,nxmap)
            do i=1,nxmap
               TpracticalXY(i,j)=10.d0**TpracticalXY(i,j)
            end do
         end do

 800     format(f18.8,A2,A2,A13,f18.8,A26,i12,A37,f18.8,A30,f18.8,A34)
         ifilter=1
         do
            read(72,800,end=200) mag(ifilter),dc2,filtername(ifilter),
     $           dc13,wavelength(ifilter),dc26,dummy,dc37,
     $           totalfluxdensity(ifilter),dc30,absoluteflux(ifilter),
     $           dc34
            wavelength(ifilter)=wavelength(ifilter)/1d4
            do j=1,nymap
               read(72,'(2001g11.4)') (fluxdensityXY(i,j,ifilter),
     $              i=1,nxmap)
               do i=1,nxmap
                  fluxdensityXY(i,j,ifilter)=
     $                 10.d0**fluxdensityXY(i,j,ifilter)
               end do
            end do
            ifilter = ifilter + 1
         end do
 200     close(72)
         
         numfilters = ifilter-1
         
         
         open(60,file=trim(adjustl(outfile)),action='write',
     $        position='append')
         write(60,*) innit,(mag(ifilter),ifilter=1,numfilters)
         close(60)

      end do
      end program
      
