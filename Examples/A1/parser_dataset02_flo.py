import matplotlib.pyplot as plt
from matplotlib import cycler
import matplotlib as mpl
import math
import numpy as np

import scipy as scipy
import scipy.odr as odr

#START styles
plt.style.use('classic')

mpl.rcParams["figure.facecolor"] = '#FFFFFF'

colors = cycler('color',
                ['#EE6666', '#3388BB', '#9988DD',
                 '#EECC55', '#88BB44', '#FFBBBB'])
plt.rc('axes', facecolor='#E6E6E6', edgecolor='none',
       axisbelow=True, grid=True, prop_cycle=colors)
plt.rc('grid', color='w', linestyle='solid')
plt.rc('xtick', direction='out', color='gray')
plt.rc('ytick', direction='out', color='gray')
plt.rc('patch', edgecolor='#E6E6E6')
plt.rc('lines', linewidth=2)

#END styles

c = 299792456.2/1.0003

def uncert_voltage(value,digits):
    #start device uncert
    digit_error = 10*10**(-digits)
    output = abs(value/100*0.05) + digit_error
    #end device uncert
    #start human error
    additional_error = abs(value/100)
    output += additional_error
    #end human error
    return output

def wavelength_to_frequency(wavelength):
    return c/(wavelength*10**(-9))

def linear_func(p, x):  
   a, b = p  
   return a * x + b 

def perform_odr(x, y, yerr):
    """Finds the ODR for data {x, y} and returns the result"""
    linear = odr.Model(linear_func)
    mydata = odr.RealData(x, y, sy=yerr)
    myodr = odr.ODR(mydata, linear, beta0=[4*10**(-15),-1.2], maxit=1000000000)
    output = myodr.run()
    return output

files = ["dataset02_flo.ini"]

voltages = []
voltages_uncerts = []
frequencies = []
frequencies_uncerts = []

clean_values = []

with open(files[0]) as f:
    for line in f:
        clean_values.clear()
        digits = 0
        for index, value in enumerate(line.split(",")):
            clean_values.append(float(value.rstrip()))
            if index == 1:
                decimals = value.rstrip()[value.find("."):]
                digits = len(decimals)-1
        frequencies.append(wavelength_to_frequency(clean_values[0]))
        frequencies_uncerts.append(0)
        voltages.append(-clean_values[1])
        voltages_uncerts.append(uncert_voltage(-clean_values[1],digits))
        print("Spannung: (%f +/- %f)V, Frequenz: %fHz" % (-clean_values[1],uncert_voltage(-clean_values[1],digits),wavelength_to_frequency(clean_values[0])))

data = np.array([frequencies,frequencies_uncerts,voltages,voltages_uncerts])
sorted_data = data[:, data[0].argsort()]

#plt.plot(sorted_data[0],sorted_data[1], marker='o',color='r', linestyle="none", alpha=0.2, label="")
plt.errorbar(sorted_data[0],sorted_data[2],yerr=sorted_data[3],marker='x',linestyle="none")
plt.xlabel("Frequenz in Hz")
plt.ylabel("E$_{kin}$ in eV")

x = np.asarray(sorted_data[0])
xerr = np.asarray(sorted_data[1])
y = np.asarray(sorted_data[2])
yerr = np.asarray(sorted_data[3])

#obj = LinearReg(x,y,yerr)
#obj.describe()

#plt.plot(xfine, obj.Slope*xfine + obj.Intersect, alpha=0.25,color='blue', label="Lineare Regressionsgerade")

regression = perform_odr(x, y, yerr)
regression.pprint()
plt.plot(x, linear_func(regression.beta,x), alpha=0.25,color='blue', label="Lineare Regressionsgerade")

plt.legend(loc='lower left', bbox_to_anchor= (0.0, 1.01), ncol=2,
            borderaxespad=0, frameon=False)
plt.savefig("Data02_flo.png")
plt.show()

print("h = (%f*e-34 +/- %f*e-34)Js" % (regression.beta[0]*10**(15)*1.602176565,regression.sd_beta[0]*10**(15)*1.602176565))
print("W_A = (%f +/- %f)J" % (regression.beta[1],regression.sd_beta[1]))
print("Chi^2 = %f" % (regression.res_var))