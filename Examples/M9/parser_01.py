import matplotlib.pyplot as plt
from matplotlib import cycler
import matplotlib as mpl
import math
import numpy as np

g = 9.812568480
rho_L = 1.29
rho = 7850

def my(data):# arithmetic mean
    output = 0.0
    for x_i in data:
        output += x_i
    output /= len(data)
    return output

def KI(data):
    output = 0.0
    output = sigma(data)/math.sqrt(len(data))
    return output

def sigma(data): #standard deviation
    output = 0.0
    for x_i in data:
        output += np.square(x_i-my(data))
    output /= (len(data)-1)
    output = math.sqrt(output)
    return output

def period_duration(phi,order):
    output = 0
    for n in range(0,order):
        top = math.factorial(2*n)
        bottom = (2**n*math.factorial(n))**2
        term = math.sin(phi/2)**(2*n)
        output = output + (top/bottom)**2*term
    return output

def uncert_length(length_in_mm):
    return 0.02+(0.00005*length_in_mm)

def uncert_additional_length():
    return 0.03

def uncert_periodtime(periodtime):
    return 0.001+(0.000001*periodtime)

def uncert_ring_distance():
    return 0.05*20

def uncert_turns():
    return 0.05

def uncert_amp(length,distance,height_diff,u_lr,u_d,u_h):
    first_term = (length-height_diff)/(distance**2+(length-height_diff)**2)*u_d
    second_term = distance/(distance**2+(length-height_diff)**2)*u_lr
    third_term = distance/(distance**2+(length-height_diff)**2)*u_h
    return math.sqrt(first_term**2+second_term**2+third_term**2)

def uncert_T_calc(length,u_lr):
    return (math.pi/math.sqrt(length*g))*u_lr

def uncert_T_phi_calc(order,T_phi,T,phi,u_T,u_phi):
    first_term = (T_phi*u_T)**2
    second_term = 0
    for k in range(0,order):
        top = math.factorial(2*k)*(k*(math.sin(phi/2)**(2*k-1))*math.cos(phi/2))
        bottom = (2**k)*math.factorial(k)**2
        second_term = second_term + (top/bottom)
    second_term = T*second_term*u_phi
    second_term = second_term**2
    return math.sqrt(first_term+second_term)

def uncert_g(T,l_r,u_T,u_lr):
    first_term = (-8*math.pi**2*l_r/T**3)*u_T
    second_term = (4*math.pi**2*l_r/T**2)*u_lr
    return math.sqrt(first_term**2+second_term**2)

def uncert_gc(g_c,T_phi,T,l_r,phi,u_T,u_lr,u_phi):
    first_term = -2/T*g_c*u_T
    second_term = ((2*math.pi/T_phi)**2*(1+phi**2/8+(rho_L/rho)))*u_lr
    third_term = (2*math.pi/T_phi)**2*l_r*phi/4*u_phi
    return math.sqrt(first_term**2+second_term**2+third_term**2)

def uncert_distances():
    return 0.001

def uncert_height():
    return 0.001

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
u_y1 = []
u_y2 = []
clean_values = []
with open(files[0]) as f:
    for line in f:
        clean_values.clear()
        for value in line.split(","):
            clean_values.append(float(value.rstrip()))
        x.append(clean_values[0]*20)
        y_1.append(clean_values[1])
        y_2.append(clean_values[2])
        u_y1.append(uncert_periodtime(clean_values[1]))
        u_y2.append(uncert_periodtime(clean_values[2]))
        print("Abstand zur Startposition: (%f +/- %f)mm" % (clean_values[0]*20,uncert_ring_distance()))
        print("Doppelte Periodendauer (Schneide 1) in s: (%f +/- %f)" % (clean_values[1],uncert_periodtime(clean_values[1])))
        print("Doppelte Periodendauer (Schneide 2) in s: (%f +/- %f)" % (clean_values[2],uncert_periodtime(clean_values[2])))

plt.plot(x,y_1, marker='',color='r', linestyle="none", alpha=0.2, label="Schneide 1")
plt.plot(x,y_2, marker='',color='g', linestyle="none", alpha=0.2, label="Schneide 2")
plt.errorbar(x,y_1,color='r',xerr=uncert_ring_distance(),yerr=u_y1,linestyle="none")
plt.errorbar(x,y_2,color='g',xerr=uncert_ring_distance(),yerr=u_y2,linestyle="none")
plt.xlabel("Abstand zur Startposition in mm")
plt.ylabel("Doppelte Periodendauer in s")

plt.legend()
plt.show()

files_2 = ["dataset02_lks.ini"]

x_2 = []
y_2_1 = []
y_2_2 = []
u_y21 = []
u_y22 = []
clean_values_2 = []
with open(files_2[0]) as f:
    for line in f:
        clean_values_2.clear()
        for value in line.split(","):
            clean_values_2.append(float(value.rstrip()))
        x_2.append(clean_values_2[0])
        y_2_1.append(clean_values_2[1])
        y_2_2.append(clean_values_2[2])
        u_y21.append(uncert_periodtime(clean_values_2[1]))
        u_y22.append(uncert_periodtime(clean_values_2[2]))
        print("Umdrehungen: (%f +/- %f)" % (clean_values_2[0],uncert_turns()))
        print("Zehnfache Periodendauer (Schneide 1) in s: (%f +/- %f)" % (clean_values_2[1],uncert_periodtime(clean_values_2[1])))
        print("Zehnfache Periodendauer (Schneide 2) in s: (%f +/- %f)" % (clean_values_2[2],uncert_periodtime(clean_values_2[2])))

plt.plot(x_2,y_2_1, marker='',color='r', linestyle="none", alpha=0.2, label="Schneide 1")
plt.plot(x_2,y_2_2, marker='',color='g', linestyle="none", alpha=0.2, label="Schneide 2")
plt.errorbar(x_2,y_2_1,color='r',xerr=uncert_turns(),yerr=u_y21,linestyle="none")
plt.errorbar(x_2,y_2_2,color='g',xerr=uncert_turns(),yerr=u_y22,linestyle="none")
plt.xlabel("Umdrehungen des Gewichts")
plt.ylabel("Zehnfache Periodendauer in s")
plt.ticklabel_format(useOffset=False)
plt.legend()
plt.show()

files_3 = ["dataset03_lks.ini"]
data_length = []
with open(files_3[0]) as f:
    for line in f:
        data_length.append(float(line.rstrip()))
        print("Gemessene Länge: (%f +/- %f)mm" % (float(line.rstrip()),uncert_length(float(line.rstrip()))))
plt.hist(data_length, bins=len(data_length)*2)

length_mean = my(data_length)
uncert_length = uncert_length(length_mean)
additional_length = 10.03
print("Mittelwert Länge: (%f +/- %f) mm" % (length_mean,uncert_length))

ki_value = KI(data_length)
s_value = sigma(data_length)

print("Mittelwert Länge verrechnet: (%f +/- %f) mm" % (length_mean+additional_length,math.sqrt((uncert_length**2)+(uncert_additional_length()**2))))
y_max = plt.gca().get_ylim()[1]
plt.vlines(length_mean,ymin=0, ymax=y_max, label='Mittelwert', ls=':', lw=2, colors='purple')

plt.vlines(x=length_mean-s_value, ymin=0, ymax=y_max, label='Standardabweichung', ls=':', lw=2, colors='green')
plt.vlines(x=length_mean+s_value, ymin=0, ymax=y_max, label='Standardabweichung', ls=':', lw=2, colors='green')

plt.vlines(x=length_mean-ki_value, ymin=0, ymax=y_max, label='Vertrauensbereich', ls=':', lw=2, colors='red')
plt.vlines(x=length_mean+ki_value, ymin=0, ymax=y_max, label='Vertrauensbereich', ls=':', lw=2, colors='red')

print("Vertrauensbereich: %fmm , sqrt(Vertrauensbereich^2 + 1^2)mm = %fmm" % (ki_value,math.sqrt(ki_value**2 + (uncert_distances()*1000)**2)))

plt.ticklabel_format(useOffset=False)
plt.legend()
plt.show()

files_4 = ["dataset04_lks.ini"]

read_height = 0

with open(files_4[0]) as f:
    for line in f:
        read_height = float(line.rstrip())

length_mean += additional_length
adj_leg = length_mean - read_height

length_mean = length_mean / 1000
adj_leg = adj_leg / 1000

files_5 = ["dataset05_lks.ini"]
distances = []
period_times = []

clean_values_3 = []
with open(files_5[0]) as f:
    for line in f:
        clean_values_3.clear()
        for value in line.split(","):
            clean_values_3.append(float(value.rstrip()))
        distances.append(clean_values_3[0]/100)
        print("[AMP] Periodendauer: (%f +/- %f)s" % (clean_values_3[1],uncert_periodtime(clean_values_3[1])))
        if len(clean_values_3) > 2:
            data = [clean_values_3[1],clean_values_3[2]]
            mean = my(data)
            period_times.append(mean/10)
        else:
            period_times.append(clean_values_3[1]/10)

amps = []
t_phi = []
x_err = []
y_err_1 = []
y_err_2 = []

t_calc = 2*math.pi*math.sqrt(length_mean/g)
uncert_length_in_m = uncert_length/1000

for index, periodtime in enumerate(period_times):
    amps.append(math.atan((distances[index])/adj_leg))
    t_phi.append(t_calc*period_duration(amps[index],30))
    x_err.append(uncert_amp(length_mean,distances[index],read_height,uncert_length_in_m,uncert_distances(),uncert_height()))
    y_err_1.append(uncert_periodtime(periodtime))
    y_err_2.append(uncert_T_phi_calc(30,t_phi[index],t_calc,amps[index],uncert_T_calc(length_mean,uncert_length_in_m),x_err[index]))
    print("Periodendauer: %f - Wert für phi: %f" % (period_times[index],t_phi[index]))

plt.plot(amps,period_times, marker='', color='r', linestyle="none", alpha=0.2, label="T gemessen")
plt.plot(amps,t_phi, marker='',color='g', linestyle="solid", alpha=0.2, label="$T(\\Phi_0)$")
plt.errorbar(amps,period_times,color='r',xerr=x_err,yerr=y_err_1,linestyle="none")
plt.errorbar(amps,t_phi,color='g',xerr=x_err,yerr=y_err_2,linestyle="none")
plt.xlabel("Amplitude in rad")
plt.ylabel("Periodendauer in s")
plt.ticklabel_format(useOffset=False)
plt.legend()
plt.show()

print("g nach (4): (%f +/- %f)m/s^2" % (4*math.pi**2*length_mean/period_times[index]**2,uncert_g(period_times[index],length_mean,y_err_1[index],uncert_length_in_m)))

for index, phi in enumerate(t_phi):
    first_term_measure = (2*math.pi/period_times[index])**2
    first_term_calc = (2*math.pi/phi)**2
    second_term = (1+(amps[index]**2)/8+(rho_L/rho))
    #uncert_gc(g_c,T_phi,T,l_r,phi,u_T,u_lr,u_phi):
    calc_gc = first_term_calc*length_mean*second_term
    meas_gc = first_term_measure*length_mean*second_term
    uncert_calc_gc = uncert_gc(calc_gc,phi,t_calc,length_mean,amps[index],uncert_T_calc(length_mean,uncert_length_in_m),uncert_length_in_m,x_err[index])
    uncert_meas_gc = uncert_gc(meas_gc,period_times[index],t_calc,length_mean,amps[index],uncert_T_calc(length_mean,uncert_length_in_m),uncert_length_in_m,x_err[index])
    print("Errechnet: g_c = (%f +/- %f)m/s^2 | Gemessen: g_c = (%f +/- %f)m/s^2" % (calc_gc,uncert_calc_gc,meas_gc,uncert_meas_gc))
