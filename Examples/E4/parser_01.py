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

fig, axs = plt.subplots(2, 2)

filelist = [["dataset01_lks.ini", "dataset02_lks.ini"],["dataset01_flo.ini","dataset02_flo.ini"]]

axs[0,0].set_title("Messergebnisse: xxx")
axs[0,1].set_title("Messergebnisse: yyy")
axs[0,0].annotate("Kondensator", xy=(0, 0.5), xytext=(-axs[0,0].yaxis.labelpad - 5, 0),
                xycoords=axs[0,0].yaxis.label, textcoords='offset points',
                size='large', ha='right', va='center')
axs[1,0].annotate("Spule", xy=(0, 0.5), xytext=(-axs[1,0].yaxis.labelpad - 5, 0),
                xycoords=axs[1,0].yaxis.label, textcoords='offset points',
                size='large', ha='right', va='center')
for index,files in enumerate(filelist):

    R_P = 10
    R_P_UNCERT = 0.5

    data_01 = []
    data_02 = []

    filename = files[0][files[0].rfind("\\")+1:]
    filename = filename[0:filename.find(".")]

    clean_values = []
    with open(files[0]) as f:
        for line in f:
            clean_values.clear()
            for value in line.split(","):
                clean_values.append(float(value.rstrip()))
            data_01.append(clean_values.copy())

    with open(files[1]) as f:
        for line in f:
            clean_values.clear()
            for value in line.split(","):
                clean_values.append(float(value.rstrip()))
            data_02.append(clean_values.copy())

    freqs01 = []
    freqs_uncert01 = []
    U_C101 = []
    U_C101_fact = []
    U_C201 = []
    U_C201_fact = []

    for entry in data_01:
        freqs_uncerts = correct_freq_and_uncert(entry[0]*1000)
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

    axs[0][index].errorbar(freqs01,y1,xerr=freqs_uncert01,yerr=y1_uncert,linestyle="none")
    axs[0][index].set(ylabel="Scheinwiderstand in $\\Omega$", xlabel="Frequenz in Hz")

    freqs02 = []
    freqs_uncert02 = []
    U_C102 = []
    U_C102_fact = []
    U_C202 = []
    U_C202_fact = []

    for entry in data_02:
        freqs_uncerts = correct_freq_and_uncert(entry[0])
        freqs02.append(freqs_uncerts[0])
        freqs_uncert02.append(freqs_uncerts[1])
        U_C102.append(entry[1])
        U_C102_fact.append(entry[2])
        U_C202.append(entry[3])
        U_C202_fact.append(entry[4])

    y2 = []
    y2_uncert =[]
    for i,element in enumerate(U_C102):
        y2.append(R_P*(U_C102[i]-U_C202[i])/U_C202[i])
        y2_uncert.append(gauss_uncert(U_C102[i],U_C202[i],R_P,U_C102_fact[i]*0.2,U_C202_fact[i]*0.2,R_P_UNCERT))

    axs[1][index].errorbar(freqs02,y2,xerr=freqs_uncert02,yerr=y2_uncert,linestyle="none")
    axs[1][index].set(ylabel="Scheinwiderstand in $\\Omega$", xlabel="Frequenz in Hz")

top_left_max_y = axs[0][0].get_ylim()[1]
top_right_max_y = axs[0][1].get_ylim()[1]
bottom_left_max_y = axs[1][0].get_ylim()[1]
bottom_right_max_y = axs[1][1].get_ylim()[1]

max_top01_y = np.maximum(top_left_max_y,top_right_max_y)
max_top02_y = np.maximum(bottom_left_max_y,bottom_right_max_y)

axs[0][0].set_ylim(0,max_top01_y)
axs[0][1].set_ylim(0,max_top01_y)
axs[1][0].set_ylim(0,max_top02_y)
axs[1][1].set_ylim(0,max_top02_y)

top_left_max_x = axs[0][0].get_xlim()[1]
top_right_max_x = axs[0][1].get_xlim()[1]
bottom_left_max_x = axs[1][0].get_xlim()[1]
bottom_right_max_x = axs[1][1].get_xlim()[1]

max_top01_x = np.maximum(top_left_max_x,top_right_max_x)
max_top02_x = np.maximum(bottom_left_max_x,bottom_right_max_x)

axs[0][0].set_xlim(0,max_top01_x)
axs[0][1].set_xlim(0,max_top01_x)
axs[1][0].set_xlim(0,max_top02_x)
axs[1][1].set_xlim(0,max_top02_x)

plt.show()