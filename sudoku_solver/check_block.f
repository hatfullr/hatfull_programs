      function check_block(nblock,num)
      include 'header.f'
      integer check_block,num,nblock
      integer temp

c     Return 0 if block doesn't contain num
c     Return 1 if block does contain num

      check_block = 0
      do i=1,9
c         temp = block(nblock,i)
         do j=i+1,9
            write(*,*) block(nblock,j)
            if(block(nblock,j).eq.num) then
               check_block = 1
               return
            end if
         end do
      end do
      
      return
      end function
