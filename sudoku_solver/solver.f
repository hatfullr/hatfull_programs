      program solver
      include 'header.f'
      integer npossibilities
      integer check_block
      integer nblock
      
      puzzlefile = "puzzle.txt"
      
      write(*,*) "Reading puzzle " // trim(puzzlefile)
      call read_puzzle
      call get_blocks

c     Start at the top-left cell and determine the number of
c     possible numbers that can fit in the cell. If it's more
c     than 1, we move to the next cell.
      npossibilities=0

      write(*,*) check_block(3,1)
      
      do i=1,9
         do j=1,9
            if(puzzle(i,j).eq.0) then
               nblock = (j+2)/3 + ((i-1)/3)*3
c               write(*,*)i,j, nblock,check_block(nblock,1)
               if(check_block(nblock,puzzle(i,j)).eq.1) then
c     write(*,*) i,j,puzzle(i,j),
c     $              check_block(nblock,puzzle(i,j))
               end if
c     write(*,*) ""
            end if
         end do
      end do
         
      call check_rules

      end program
