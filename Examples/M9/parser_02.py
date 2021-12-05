import matplotlib.pyplot as plt
from matplotlib import cycler
import matplotlib as mpl
import math
import numpy
import sys
import time

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


files = ["dataset01_lks.ini"]

x = []
y_1 = []
y_2 = []

filename = files[0][files[0].rfind("\\")+1:]
filename = filename[0:filename.find(".")]

clean_values = []
with open(files[0]) as f:
    for line in f:
        clean_values.clear()
        for value in line.split(","):
            clean_values.append(float(value.rstrip()))
        x.append(clean_values[0])
        y_1.append(clean_values[1])
        y_2.append(clean_values[2])

plt.plot(x,y_1, 'ro', linestyle="dotted", label="Schneide 1")
plt.plot(x,y_2, 'go', linestyle="dotted", label="Schneide 2")
plt.xlabel("Abstand zur Startposition in cm")
plt.ylabel("Doppelte Periodendauer in s")

plt.legend()
plt.show()