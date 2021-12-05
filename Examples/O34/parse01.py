import matplotlib.pyplot as plt
from matplotlib import cycler
import matplotlib as mpl
import math
import numpy
import sys
import time

def deg_to_rad(degrees):
    return degrees * numpy.pi / 180

def gauss_uncert(gamma, delta, gamma_uncert, delta_uncert):
    first_term = (1/2*numpy.cos(deg_to_rad((gamma+delta)/2))/numpy.sin(deg_to_rad(gamma/2)))*deg_to_rad(delta_uncert)
    second_term = (numpy.sin(deg_to_rad(delta/2))/(2*numpy.cos(deg_to_rad(gamma))-2))*deg_to_rad(gamma_uncert)
    return numpy.sqrt(first_term**2+second_term**2)

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


files = ["dataset01_lks.ini", "dataset01_flo.ini"]

data_01 = []
data_02 = []

filename = files[0][files[0].rfind("\\")+1:]
filename = filename[0:filename.find(".")]

with open(files[0]) as f:
    data_01 = [float(line.rstrip()) for line in f]

filename = files[1][files[1].rfind("\\")+1:]
filename = filename[0:filename.find(".")]

with open(files[1]) as f:
    data_02 = [float(line.rstrip()) for line in f]

data = []
for i,entry in enumerate(data_01):
    data.append((data_01[i]+data_02[i])/2)

gamma = 60
gamma_uncert = 5/60
delta_uncert = 5/60
n = []

lambda_arr = [404.656,435.833,491.607,546.074,579,623.440]

color_arr = ["m","b","c","g","tab:orange","r"]

uncert_delta_min = []

for i,delta_min in enumerate(data):
    uncert_delta_min.append(gauss_uncert(gamma,delta_min,gamma_uncert,delta_uncert))
    n.append(numpy.sin(deg_to_rad(1/2*(delta_min+gamma)))/numpy.sin(deg_to_rad(1/2*gamma)))
    plt.errorbar(lambda_arr[i], n[i], yerr=uncert_delta_min[i], color=color_arr[i])
    plt.errorbar(lambda_arr[i], n[i], yerr=uncert_delta_min[i], color=color_arr[i])

plt.plot(lambda_arr,n, "or")

print("Lila: n = ",n[0], "+/-", uncert_delta_min[0],"\n")
print("Blau: n = ",n[1], "+/-", uncert_delta_min[1],"\n")
print("Zyan: n = ",n[2], "+/-", uncert_delta_min[2],"\n")
print("Grün: n = ",n[3], "+/-", uncert_delta_min[3],"\n")
print("Orange: n = ",n[4], "+/-", uncert_delta_min[4],"\n")
print("Rot: n = ",n[5], "+/-", uncert_delta_min[5],"\n")

dataset02_file = ["dataset02_lks.ini"]

filename = dataset02_file[0][dataset02_file[0].rfind("\\")+1:]
filename = filename[0:filename.find(".")]

with open(dataset02_file[0]) as f:
    data2_01 = [float(line.rstrip()) for line in f]

value = numpy.sin(deg_to_rad(1/2*(data2_01[0]+gamma)))/numpy.sin(deg_to_rad(1/2*gamma))
uncert = gauss_uncert(gamma,data2_01[0],gamma_uncert,delta_uncert)
print("Natrium: ", value, "+/-", uncert, "\n")

na_x = [588.9950,589.5924]
na_y = [value,value]
na_uncert = [uncert,uncert]
#plt.plot(na_x,na_y, "x", label="Natrium")
plt.errorbar(na_x, na_y, yerr=na_uncert, color=color_arr[i],label="Natrium")

ax = plt.gca()
ax.ticklabel_format(useOffset=False)

x = numpy.linspace(400,700,100)

B_1 = 1.34533359
B_2 = 0.209073176
B_3 = 0.937357162
C_1 = 0.00997743871*1000000
C_2 = 0.0470450767*1000000
C_3 = 111.8867640*1000000

y = numpy.sqrt(1+(B_1*x**2)/(x**2-C_1)+(B_2*x**2)/(x**2-C_2)+(B_3*x**2)/(x**2-C_3))

d_lambda = ((2*B_3*590)/( 590**2-C_3)-(2*B_3*590**3)/(590**2-C_3)**2+(2*B_2*590)/(590**2-C_2)-(2*B_2*590**3)/(590**2-C_2)**2+(2*B_1*590)/(590**2-C_1)-(2*B_1*590**3)/(590**2-C_1)**2)/(2*numpy.sqrt((B_3*590**2)/(590**2-C_3)+(B_2*590**2)/(590**2-C_2)+(B_1*590**2)/(590**2-C_1)+1))
print("D_LAMBDA:", -0.0275*d_lambda)

plt.plot(x,y,label="Sellmeier-Modellfunktion")

plt.legend()
plt.show()