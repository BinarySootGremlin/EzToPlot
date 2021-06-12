def digit_uncert(value, uncert):
    if(value.find(".") >= 0):
        return uncert * 10**(-((len(value)-1) - value.find(".")))
    else:
        return uncert

def resolution_uncert(res, percent):
    return (res/100)*percent

def percent_uncert(value, percent):
    return (value/100)*percent