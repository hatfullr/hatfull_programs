# Makefile for flux_cal
# Use gfortran because it's more standard
FC = $(shell which gfortran)
FFLAGS = -O4 -ffixed-line-length-132

LIB = -L/usr/lib

executable = getFiltersFromFluxes

objects = $(executable).o 

$(executable): $(objects)
	$(FC) -o $(executable) $(objects) $(LIB)


# Delete all made stuff
clean:
	@\rm -rf $(objects) $(executable)


