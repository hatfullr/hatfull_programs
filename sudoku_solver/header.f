      implicit none
      character*255 puzzlefile
      logical puzzleexist
      integer i,j,k,sbi,sbj,a
      
      integer nrules
      parameter(nrules=3)

      integer rule(nrules)

      integer puzzle(9,9)
      integer block(9,9)
      
      common/a/ puzzlefile
      common/b/ puzzleexist
      common/c/ puzzle
      common/d/ rule
      common/e/ block
      
