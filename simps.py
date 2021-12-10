# Simpson's rule integration
import numpy as np
from scipy.interpolate import interp1d

def simps(x,y,xlim=(None,None)):
    x = np.array(x)
    y = np.array(y)
    if xlim[0] is not None:
        if xlim[0] in x:
            i = np.arange(len(x))[x==xlim[0]]
            if any(i):
                i = i[0]
                x = x[i:]
                y = y[i:]
            else:
                raise RuntimeError("Something went wrong while trying to find xlim[0] in x")
        else:
            # Find the closest lower bound
            for i, elem in enumerate(x):
                if elem > xlim[0]:
                    f = interp1d(x,y)
                    x = np.append([xlim[0]],x[i:])
                    y = np.append([f(xlim[0])],y[i:])
                    break
            else:
                raise ValueError("Keyword 'xlim' contains a lower bound outside the given x data.")
    if xlim[1] is not None:
        if xlim[1] in x:
            i = np.arange(len(x))[x==xlim[1]]
            if any(i):
                i = i[0]
                x = x[:i+1]
                y = y[:i+1]
            else:
                raise RuntimeError("Something went wrong while trying to find xlim[1] in x")
        else:
            # Find the closest upper bound
            for i in range(-len(x),0):
                if x[i] < xlim[1]:
                    f = interp1d(x,y)
                    x = np.append(x[:i+1],[xlim[1]])
                    y = np.append(y[:i+1],[f(xlim[1])])
                    break
            else:
                raise ValueError("Keyword 'xlim' contains a lower bound outside the given x data.")
        
    dx = np.diff(x)
    result = np.full(len(y)-1,np.nan)
    y1 = y[0]
    d = 0
    for i,y2 in enumerate(y[1:]):
        d += 0.5*(y1+y2)*dx[i]
        result[i] = d
        y1 = y2
    return result


# To test the code
if __name__ == "__main__":
    import warnings
    warnings.filterwarnings("ignore")

    def print_result(label,test,analytic):
        print("%20s: test = %10g, analytic = %10g, difference = %6.2f%%" % (label,test[-1],analytic,abs(test[-1]-analytic)/analytic * 100))
    
    x = np.linspace(0,1,101)
    
    # Linear unbounded
    test = simps(x,x)
    analytic = 0.5*(x[-1]**2-x[0]**2)
    print_result("linear",test,analytic)

    # Linear bounded w/ limits pre-existing within x array
    test = simps(x,x,xlim=(x[25], x[60]))
    analytic = 0.5*(x[60]**2-x[25]**2)
    print_result("linear, limits 1",test,analytic)

    # Linear bounded w/ limits not pre-existing within x array
    test = simps(x,x,xlim=(0.1235,0.8176))
    analytic = 0.5*(0.8176**2 - 0.1235**2)
    print_result("linear, limits 2",test,analytic)

    # Simple sin function, unbounded
    test = simps(x,np.sin(np.pi * x))
    analytic = (np.cos(np.pi * x[0]) - np.cos(np.pi * x[-1])) / np.pi
    print_result("sin(pi x)",test,analytic)

    # 1/x function; steep vertically and horizontally
    test = simps(x,1/x,xlim=(0.1,1))
    analytic = np.log(1) - np.log(0.1)
    print_result("1/x from 0.1 to 1",test,analytic)
    
    # 1/x^2
    test = simps(x,1/x**2,xlim=(0.1,1))
    analytic = 1./0.1 - 1
    print_result("1/x^2 from 0.1 to 1",test,analytic)
    
    # 1/x^3
    test = simps(x,1/x**3,xlim=(0.1,1))
    analytic = 0.5 * (1./0.1**2 - 1)
    print_result("1/x^3 from 0.1 to 1",test,analytic)

    # 1/x^4
    test = simps(x,1/x**4,xlim=(0.1,1))
    analytic = 1./3. * (1./0.1**3 - 1)
    print_result("1/x^4 from 0.1 to 1",test,analytic)
    
    # 1/x^5
    test = simps(x,1/x**5,xlim=(0.1,1))
    analytic = 0.25 * (1./0.1**4. - 1)
    print_result("1/x^5 from 0.1 to 1",test,analytic)
    
