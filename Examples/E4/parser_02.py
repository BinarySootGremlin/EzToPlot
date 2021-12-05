import matplotlib.pyplot as plt
from matplotlib import cycler
import matplotlib as mpl
import numpy as np

import math
def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper

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

def gauss_uncert(U_c1, U_c2, R_P, U_c1_uncert, U_c2_uncert, r_p_uncert):
    U_c1_deriv = R_P/U_c2
    U_c2_deriv = -(R_P*U_c1)/(U_c2**2)
    R_P_deriv = (U_c1-U_c2)/U_c2 
    return np.sqrt((U_c1_deriv*U_c1_uncert)**2+(U_c2_deriv*U_c2_uncert)**2+(R_P_deriv*r_p_uncert)**2)

def correct_freq_and_uncert(freq,additional_uncert = 0):
    return [freq,freq/100*5]

fig, axs = plt.subplots(nrows=1, ncols=2)

filelist = ["dataset03_lks.ini", "dataset03_flo.ini"]

axs[0].set_title("Messergebnisse: xxx")
axs[1].set_title("Messergebnisse: yyy")

for index,file in enumerate(filelist):

    R_P = 10
    R_P_UNCERT = 0.5

    data_01 = []

    filename = file[file.rfind("\\")+1:]
    filename = filename[0:filename.find(".")]

    clean_values = []
    with open(file) as f:
        for line in f:
            clean_values.clear()
            for value in line.split(","):
                clean_values.append(float(value.rstrip()))
            data_01.append(clean_values.copy())

    data_01.sort()

    freqs01 = []
    freqs_uncert01 = []
    U_C101 = []
    U_C101_fact = []
    U_C201 = []
    U_C201_fact = []

    for entry in data_01:
        freqs_uncerts = correct_freq_and_uncert(entry[0])
        freqs01.append(freqs_uncerts[0])
        freqs_uncert01.append(freqs_uncerts[1])
        U_C101.append(entry[1])
        U_C101_fact.append(entry[2])
        U_C201.append(entry[3])
        U_C201_fact.append(entry[4])

    y1 = []
    y1_uncert = []
    for i,element in enumerate(U_C101):
        y1.append(R_P*(U_C101[i]-U_C201[i])/U_C201[i])
        y1_uncert.append(gauss_uncert(U_C101[i],U_C201[i],R_P,U_C101_fact[i]*0.2,U_C201_fact[i]*0.2,R_P_UNCERT))

    axs[index].errorbar(freqs01,y1,xerr=freqs_uncert01,yerr=y1_uncert,linestyle="none")
    axs[index].set(ylabel="Scheinwiderstand in $\\Omega$", xlabel="Frequenz in Hz")
    print("freq: ")
    print(freqs01)
    print("freq_uncert: ")
    print(freqs_uncert01)
    print("z: ")
    print(y1)
    print("z_uncert: ")
    print(y1_uncert)

left_max_y = axs[0].get_ylim()[1]
right_max_y = axs[1].get_ylim()[1]

max_top01_y = np.maximum(left_max_y,right_max_y)

axs[0].set_ylim(0,max_top01_y)
axs[1].set_ylim(0,max_top01_y)

left_max_x = axs[0].get_xlim()[1]
right_max_x = axs[1].get_xlim()[1]

max_top01_x = np.maximum(left_max_x,right_max_x)

axs[0].set_xlim(0,max_top01_x)
axs[1].set_xlim(0,max_top01_x)

plt.title="Schwingkreis"
plt.show()