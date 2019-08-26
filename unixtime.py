# Written by Roger Hatfull 11/06/2018
# University of Alberta

def to_unix(year=1970,month=1,day=1,hour=0,minute=0,second=0):
    # Every day has 86400 seconds
    # A leap year happens if these criteria are met:
    #    - The year can be evenly divided by 4
    #    - If the year can be evenly divided by 100, it is NOT a leap
    #      year, unless the year is also evenly divisible by 400. Then it
    #      is a leap year.

    def isleap(y):
        leap = False
        if y%4 == 0: # Evenly divided by 4
            leap = True
            if y%100 == 0: # Evenly divided by 100
                leap = False
                if y%400 == 0: # Evenly divided by 400
                    leap = True
        return leap

    daym = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ]

    if isleap(year): daym[1]+=1
    
    dyear = year - 1970

    dday = dyear*365.25 + sum(daym[:month-1]) + day - 1
    return dday*86400 + hour*60.*60. + minute*60. + second
