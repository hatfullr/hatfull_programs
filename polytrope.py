"""
This class defines a polytropic stellar model.
n is the polytopic index

The equation to solve is d^2y/dx^2 = -(y^n + 2/x dy/dx)
where y is the dimensionless density and x is the
dimensionless distance from center.

Author: Roger Hatfull
University of Alberta
"""
import numpy as np
from scipy.optimize import newton

class Polytrope(dict,object):
    G = 6.67390e-8
    a = 4.*5.670374e-5 / 29979245800.
    kboltz = 1.380649e-16
    mH = 1.00784 / 6.0221409e23
    
    def __init__(self,n,rhoc,Pc,mu,precision=1.e-3):
        super(Polytrope,self).__init__()
        self.n = n
        self.rhoc = rhoc
        self.Pc = Pc
        self.mu = mu
        self.precision = precision
        
        self.lamb = np.sqrt((self.n+1) / (4*np.pi*Polytrope.G) * self.Pc * self.rhoc**(-2.))

    def dimensionless_density(self,r):
        # Obtain the value of the dimensionless density at location xi
        if not isinstance(r,(list,tuple,np.ndarray)):
            xi = r / self.lamb
            dxi = self.precision
            xi0 = 0.
            y = 1.
            dydxi = 0.
            while y > 0. and xi0 < xi:
                if xi0+dxi > xi: dxi = (xi-xi0)
                dydxi -= (y**self.n + 2./(xi0+dxi)*dydxi)*dxi
                y += dydxi*dxi
                xi0 += dxi
            return y
        else:
            r = np.array(r)
            y = np.empty(len(r))
            for i,ri in enumerate(r):
                y[i] = self.dimensionless_density(ri)
            return y
            
        
        
    def density(self,x):
        # x is distance from the center of the polytrope
        return self.rhoc * self.dimensionless_density(x)**self.n

    def temperature(self,x):
        # Using P = rho kboltz T / (mu mH) + 1/3 a T^4,
        # we recast this as (mu mH Pc)/(kboltz rhoc) * Dn = (1 + (a mu mH)/(3 kboltz) T^3) T,
        # where Pc is the central pressure, rhoc is the central density, and a=4sigma/c is
        # the radiation constant. Dn is the dimensionless density.
        
        # Get the dimensionless density at x
        Dn = self.dimensionless_density(x)
        
        const1 = Polytrope.a * self.mu*Polytrope.mH / (3.*Polytrope.kboltz)
        const2 = - (self.mu * Polytrope.mH * self.Pc) / (Polytrope.kboltz * self.rhoc) * Dn
        
        def f(T): return T + const1 * T**4. + const2
        def dfdT(T): return 1. + 3*const1*T**3.

        # Take initial guess as ideal gas only:
        return newton(f,const2,fprime=dfdT)
        

# For testing:
"""
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from fastfileread import FastFileRead

    data = FastFileRead(
        "/home/hatfull/data/hong/dynamical/d005h_d023c_b031c_R37N3_newStarSmasher_300k_nnopt79_point_mass_close_start_continuation_ncooling1_full_analysis/fluxcal_track/fluxcal_1849.track",
        header=1,
        binary_format='<'+19*'f8,'+'i4',
        offset=4,
        return_type=dict,
        parallel=False,
        verbose=True,
    )[0]
    ID = 299381
    
    fig,ax = plt.subplots(dpi=300)
    ax.set_xlim(0.,10.)
    ax.set_ylim(0.,1.05)
    
    x = 2.*data['h'][data['ID'] == ID+1][0]
    print("x =",x)
    rhoc = data['rho'][data['ID'] == ID+1][0]
    Pc = data['P'][data['ID'] == ID+1][0]
    mu = data['mu'][data['ID'] == ID+1][0]/Polytrope.mH
    p = Polytrope(1,rhoc,Pc,mu)
    d = p.density(x)
    print("Density =",d)
    print("Temperature =",p.temperature(x))
    
    ax.scatter(x/p.lamb,(d/p.rhoc)**(1./p.n),label="$n="+str(p.n)+"$",s=10)
    
    #x = np.linspace(0.,np.sqrt(6),100)
    #ax.plot(x,1.-x**2./6.,linestyle='--',label="analytic n=0",zorder=-np.inf)
    my_x = np.linspace(0.,np.pi,100)
    ax.plot(my_x,np.sin(my_x)/my_x,linestyle='--',label="analytic n=1",zorder=-np.inf)
    my_x = np.linspace(0.,x/p.lamb,100)
    ax.plot(my_x,(1.+my_x**2./3.)**(-0.5),linestyle='--',label="analytic n=5",zorder=-np.inf)
    
    ax.legend()
    plt.show()
"""
