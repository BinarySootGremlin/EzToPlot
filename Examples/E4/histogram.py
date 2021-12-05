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

#START calculation formulas
def KI(data):
    output = 0.0
    output = sigma(data)/numpy.sqrt(len(data))
    return output

def N(n):# class Number
    output = 5*math.log10(n)# DIN 1302 says that lg == log10
    return output

def k(x, data):# number of appearance
    output = data.count(x)
    return output

def h(x, data):# rel frequency
    output = k(x, data)/len(data)
    return output

def my(data):# arithmetic mean
    output = 0.0
    for x_i in data:
        output += x_i
    output /= len(data)
    return output

def sigma(data): #standard deviation
    output = 0.0
    for x_i in data:
        output += numpy.square(x_i-my(data))
    output /= (len(data)-1)
    output = numpy.sqrt(output)
    return output

def phi(x, data): #gauss function
    my_value = my(data)
    sigma_value = sigma(data)
    output = numpy.exp(-(numpy.square(x-my_value))/(2*numpy.square(sigma_value)))/(numpy.sqrt(2*numpy.pi)*sigma_value)
    return output
#END gauss bell

try:
    droppedFile = sys.argv[1] 
except IndexError:
    print("No file dropped")
    droppedFile = input("filename (without .ini): ") + ".ini"

filename = droppedFile[droppedFile.rfind("\\")+1:]
filename = filename[0:filename.find(".")]

with open(droppedFile) as f:
    data_n = [float(line.rstrip()) for line in f]

r_y_t = data_n[0]
data = data_n[1:]

#START calculate delta x (p.23 of pdf)
n = len(data)
N = N(n) 
x_max = numpy.max(data)
x_min = numpy.min(data)
x_range = x_max-x_min
delta_x = x_range/N
#END caulcate
ki = KI(data)
title = input("Title: ")
x_label = "Resonanzfrequenz in Hz"
y_label = "Absolute Häufigkeit"

plt.title(title)
plt.xlabel(x_label)
plt.ylabel(y_label)
bin_count = numpy.arange(min(data), max(data) + delta_x, delta_x)
plt.hist(data, bins=bin_count)
plt.ticklabel_format(useOffset=False)
#plt.savefig(filename + '.png')

x = numpy.linspace(min(data)-(delta_x/2),max(data)+(3*delta_x/2),100)

#plt.plot(x,phi(x,data))
#plt.savefig(filename + '_gauss.png')

my_value = my(data)
ki_value = KI(data)
s_value = sigma(data)
y_max = plt.gca().get_ylim()[1]

plt.vlines(x=my_value-s_value, ymin=0, ymax=y_max, label='Standardabweichung', ls=':', lw=2, colors='green')
plt.vlines(x=my_value+s_value, ymin=0, ymax=y_max, label='Standardabweichung', ls=':', lw=2, colors='green')

plt.vlines(x=my_value, ymin=0, ymax=y_max, label='Mittelwert', ls=':', lw=2, colors='purple')

plt.legend()
#plt.savefig(filename + '_areas.png')

plt.show()
print("Mittelwert: %f, Standardabweichung: %f, y-t Wert: %f" % (my_value,s_value,r_y_t))