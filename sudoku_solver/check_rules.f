      subroutine check_rules
      include 'header.f'

      integer sqlist(9)
      integer temp
      
c     Initialize the rule flags
      do i=1,nrules
         rule(i) = 0
      end do

c     rule = 0 means rule has not been broken
c     rule = 1 means rule has been broken
      
c     Rule #1
c     Each row must have 1 and only 1 of each number from 1-9
c     9+8+7+6+5+4+3+2+1=45
      do i=1, 9
         do j=1, 9
            if(puzzle(i,j).gt.0) then
               do k=j+1,9
                  if(puzzle(i,k).gt.0) then
                     if(puzzle(i,j).eq.puzzle(i,k)) then
                        rule(1) = 1
                     end if
                  end if
               end do
            end if
         end do
      end do


c     Rule #2
c     Each column must have 1 and only 1 of each number from 1-9
      do j=1, 9
         do i=1, 9
            if(puzzle(i,j).gt.0) then
               do k=i+1,9
                  if(puzzle(k,j).gt.0) then
                     if(puzzle(i,j).eq.puzzle(k,j)) then
                        rule(2) = 1
                     end if
                  end if
               end do
            end if
         end do
      end do

c     Rule #3
c     Each sub-block must have 1 and only 1 of each number from 1-9

      call get_blocks

      do k=1,9
         do i=1,9
            temp = block(k,i)
            do j=i+1,9
               if((temp.eq.block(k,j)).and.(block(k,j).ne.0)) then
                  rule(3) = 1
               end if
            end do
         end do
      end do
      
      return
      end subroutine
