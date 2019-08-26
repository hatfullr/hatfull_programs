      subroutine read_puzzle
      include 'header.f'
      
      inquire(file=trim(puzzlefile),exist=puzzleexist)
      if(.not. puzzleexist) then
         write(*,*) "Could not find puzzlefile " // trim(puzzlefile)
         error stop
      end if

 100  format(9I2)

      open(8,file=trim(puzzlefile),status='old')
      do i=1,9
         read(8,100) (puzzle(i,j),j=1,9)
      end do

      
      end subroutine
