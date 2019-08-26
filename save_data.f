      program save_data
      include 'starsmasher.h'
      !implicit none
      character(1000) simdir, filename
      logical exist
      integer i,k,istemp

      real*8 divv(nmax)
      common/commdivv/divv
      common /jumpcomm/ tjumpahead
      real*8 erad
      common/lostenergy/ erad
      real*8 displacex, displacey,displacez
      integer ndisplace
      common/displace/displacex,displacey,displacez,ndisplace

      real*8 temp,useeostable,ucgs,rhocgs,uunit

      simdir = ""
      filename = ""
      
      write(*,*) "Enter simulation directory"
      read(*,"(A)") simdir
      write(*,*) "Is the variable 'temp' existing? y=1, n=0"
      read(*,"(I)") istemp

 100  format("/out",I4.4,".sph")
 200  format(2I15,5E15.7,2I15,E15.7,I15,3E15.7,2I15,3E15.7,I15,E15.7,I,
     $     3E15.7)              !header format
 300  format(18E15.7)           !Data format without temp, ueq, and tthermal
 400  format(19E15.7)           !Data format with temp, no ueq or tthermal
 500  format(20E15.7)           !Data format without temp, with ueq and tthermal
 600  format(21E15.7)           !Data format with temp, ueq, and tthermal

      open(50, file="data/data.sph", status="replace", action="write")
      open(51, file="data/headers.sph", status="replace",
     $     action="write", form="formatted")
      do k=0, 9999
         write(filename,100) k
         write(filename,*) trim(simdir)//trim(filename)

         inquire(file=trim(filename),exist=exist)
         if (exist) then
            write(*,*) "Reading file",trim(filename)
            open(12, file=trim(filename),form="unformatted",
     $           action="read")
            read(12) ntot,nnopt,hco,hfloor,sep0,tf,dtout,nout,nit,t,
     $           nav,alpha,beta,tjumpahead,ngr,nrelax,trelax,dt,omega2,
     $           ncooling,erad,ndisplace,displacex,displacey,displacez

            write(51,200)ntot,nnopt,hco,hfloor,sep0,tf,dtout,nout,
     $           nit,t,nav,alpha,beta,tjumpahead,ngr,nrelax,trelax,dt,
     $           omega2,ncooling,erad,ndisplace,displacex,displacey,
     $           displacez

            if(istemp.eq.1) then
               if(ncooling.eq.0) then
                  do i=1, ntot
                     read(12) x(i),y(i),z(i),am(i),hp(i),rho(i),
     $                    vx(i),vy(i),vz(i),vxdot(i),vydot(i),vzdot(i),
     $                    u(i),udot(i), !gx(i),gy(i),gz(i),
     $                    grpot(i),meanmolecular(i),cc(i),divv(i),temp
                     write(50,400) x(i),y(i),z(i),am(i),hp(i),rho(i),
     $                    vx(i),vy(i),vz(i),vxdot(i),vydot(i),vzdot(i),
     $                    u(i),udot(i), !gx(i),gy(i),gz(i),
     $                    grpot(i),meanmolecular(i),cc(i),divv(i),temp
                  end do
               else
                  do i=1, ntot
                     read(12) x(i),y(i),z(i),am(i),hp(i),rho(i),
     $                    vx(i),vy(i),vz(i),vxdot(i),vydot(i),vzdot(i),
     $                    u(i),udot(i), !gx(i),gy(i),gz(i),
     $                    grpot(i),meanmolecular(i),cc(i),divv(i),
     $                    ueq(i),tthermal(i),temp
                     write(50,600) x(i),y(i),z(i),am(i),hp(i),rho(i),
     $                    vx(i),vy(i),vz(i),vxdot(i),vydot(i),vzdot(i),
     $                    u(i),udot(i), !gx(i),gy(i),gz(i),
     $                    grpot(i),meanmolecular(i),cc(i),divv(i),
     $                    ueq(i),tthermal(i),temp
                  end do
               end if
            else
               if(ncooling.eq.0) then
                  do i=1, ntot
                     read(12) x(i),y(i),z(i),am(i),hp(i),rho(i),
     $                    vx(i),vy(i),vz(i),vxdot(i),vydot(i),vzdot(i),
     $                    u(i),udot(i), !gx(i),gy(i),gz(i),
     $                    grpot(i),meanmolecular(i),cc(i),divv(i)
                     write(50,300) x(i),y(i),z(i),am(i),hp(i),rho(i),
     $                    vx(i),vy(i),vz(i),vxdot(i),vydot(i),vzdot(i),
     $                    u(i),udot(i), !gx(i),gy(i),gz(i),
     $                    grpot(i),meanmolecular(i),cc(i),divv(i)
                  end do
               else
                  do i=1, ntot
                     read(12) x(i),y(i),z(i),am(i),hp(i),rho(i),
     $                    vx(i),vy(i),vz(i),vxdot(i),vydot(i),vzdot(i),
     $                    u(i),udot(i), !gx(i),gy(i),gz(i),
     $                    grpot(i),meanmolecular(i),cc(i),divv(i),
     $                    ueq(i),tthermal(i)
                     write(50,500) x(i),y(i),z(i),am(i),hp(i),rho(i),
     $                    vx(i),vy(i),vz(i),vxdot(i),vydot(i),vzdot(i),
     $                    u(i),udot(i), !gx(i),gy(i),gz(i),
     $                    grpot(i),meanmolecular(i),cc(i),divv(i),
     $                    ueq(i),tthermal(i)
                  end do
               end if
            end if
            
            read(12) ntot
            close(12)
            
         end if
      end do

      close(50)
      close(51)


      end program
