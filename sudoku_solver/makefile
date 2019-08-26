
FC = $(shell which gfortran)
FFLAGS = -O4 -ffixed-line-length-132
LIB = -L/usr/lib

executable = solver

objects = $(executable).o read_puzzle.o check_rules.o get_blocks.o check_block.o

$(executable): $(objects)
	$(FC) -o $(executable) $(objects) $(LIB)

clean:
	@\rm -rf $(objects) $(executable)
