      subroutine get_blocks
      include 'header.f'
      integer counter

c     Don't mess with this. It just works. Also, you're never going to
c     understand how it works.
      counter=1
      do a=1,9,3
         do k=1,9,3
            do j=k+a-1,3+k-1+a-1
               do i=k,3+k-1
                  block(counter,i-k+1+3*(j-a+1-k)) = puzzle(j-k+1,i)
               end do
            end do
            counter=counter+1
         end do
      end do
      
      return
      end subroutine
