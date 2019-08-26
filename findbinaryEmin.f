c Author: Roger Hatfull
c Dr. Jamie Lombardi
c Allegheny College
c
c This program is designed to be used in conjunction
c with starsmasher. At the point of the minimum
c energy in a binary scanning run, it is assumed that
c this is the best snapshot to start a dynamical run
c at, as mass transfer has just begun. This program
c finds that point and prints the dataline associated
c with it from energy0.sph in the working directory.
c
c The minimum E is the point of secular instability.
c That is, after this point, the stars will merge and
c before this point, they will not.

      program findbinaryEmin
      implicit none
      real*4 a,b,c,d,E,f,g,h,i
      real*4 a2,b2,c2,d2,E2,f2,g2,h2,i2
      integer Reason

      E2=1d30
      Reason=0
      open(unit=2, file="energy0.sph")
      do while (Reason .EQ. 0)
          read(2,*,IOSTAT=Reason) a,b,c,d,E,f,g,h,i
          if ((E2 .GT. E) .AND. (a .GT. 500)) then
             a2=a
             b2=b
             c2=c
             d2=d
             E2=E
             f2=f
             g2=g
             h2=h
             i2=i
          end if
      enddo
      close(unit=2)
      print *, ""
      print *, "The minimum energy of the binary is here:"
      print *, a2,b2,c2,d2,E2,f2,g2,h2,i2
      print *, ""
      end program
