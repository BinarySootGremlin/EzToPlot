import matplotlib.pyplot as plt
from matplotlib import cycler
import matplotlib as mpl
import math
import numpy as np

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

def uncert_amp(setting):
    return setting/100*1.5

files = ["dataset01_lks.ini"]

voltages = []
strengths = []
settings = []
voltages_uncerts = []
strengths_uncerts = []
clean_values = []
lowest_strength = 0
with open(files[0]) as f:
    for line in f:
        clean_values.clear()
        digits = 0
        for index, value in enumerate(line.split(",")):
            clean_values.append(float(value.rstrip()))
            if index == 0:
                decimals = value.rstrip()[value.find("."):]
                digits = len(decimals)-1
        voltages.append(clean_values[0])
        voltages_uncerts.append(uncert_voltage(clean_values[0],digits))
        strengths.append(clean_values[1]*clean_values[2])
        strengths_uncerts.append(uncert_amp(clean_values[2]))
        settings.append(clean_values[2])
        print("Spannung: (%f +/- %f)V, Stromstärke: (%f +/- %f)µA" % (clean_values[0],uncert_voltage(clean_values[0],digits),clean_values[1]*clean_values[2],uncert_amp(clean_values[2])))

data = np.array([voltages,voltages_uncerts,strengths,strengths_uncerts,settings])
sorted_data = data[:, data[0].argsort()]

lowest_strength = min(sorted_data[2])
keep_sign = False
for index, entry in enumerate(sorted_data[2]):
    if not keep_sign:
        sorted_data[2][index] = -entry
    if entry == lowest_strength:
        keep_sign = True    

plt.plot(sorted_data[0],sorted_data[2], marker='o',color='r', linestyle="solid", alpha=0.2, label="")
plt.errorbar(sorted_data[0],sorted_data[2],xerr=sorted_data[1],yerr=sorted_data[3],linestyle="none")
plt.xlabel("Spannung in V")
plt.ylabel("Stromstärke in µA")

plt.legend()
plt.savefig("Data01_lks.png")
plt.show()

plt.plot(sorted_data[0],sorted_data[2], marker='o',color='r', linestyle="solid", alpha=0.2, label="")
plt.errorbar(sorted_data[0],sorted_data[2],xerr=sorted_data[1],yerr=sorted_data[3],linestyle="none")
plt.xlabel("Spannung in V")
plt.ylabel("Stromstärke in A")
plt.xlim(-5,2)
plt.legend()
plt.savefig("Data01_lks_zoom.png")
plt.show()