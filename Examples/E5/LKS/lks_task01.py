import matplotlib.pyplot as plt
from matplotlib import cycler
import matplotlib as mpl
import numpy as np
import scipy.odr as odr

import uncert_lib

def uncert_voltage(setting):
    #start device uncert
    output = uncert_lib.resolution_uncert(setting,2.5)
    #end device uncert
    #start human error
    output += 0
    #end human error
    return output

def uncert_amp(value):
    #start device uncert
    output = uncert_lib.digit_uncert(value,1)
    output += uncert_lib.percent_uncert(float(value),1)
    #end device uncert
    #start human error
    output += 0
    #end human error
    return output

def linear_func(p, x):  
   a, b = p  
   return a * x + b 

def perform_odr(x, y, xerr, yerr):
    linear = odr.Model(linear_func)
    mydata = odr.RealData(x, y, sx=xerr, sy=yerr)
    myodr = odr.ODR(mydata, linear, beta0=[1,1], maxit=1000000000)
    output = myodr.run()
    return output

files = [["lks_no_capacitor01.ini","lks_capacitor01.ini"],["lks_no_capacitor02.ini","lks_capacitor02.ini"]]
colors = ['r','g','b','purple']
titles = ["Einweggleichrichtung","Zweiweggleichrichtung"]
labels = ["Ohne Kondensator", "Mit Kondensator"]
file_string = "LKS: \n"

wattage = []

for number, set in enumerate(files):
    plt.figure(dpi=150)
    plt.title("$" + titles[number] + "_{lks}$")
    for n, file in enumerate(set):
        voltages = []
        strengths = []
        voltages_uncerts = []
        strengths_uncerts = []
        resistance = []
        clean_values = []
        plain_values = []
        with open(file) as f:
            for line in f:
                clean_values.clear()
                plain_values.clear()
                digits = 0
                for index, value in enumerate(line.split(",")):
                    clean_values.append(float(value.rstrip()))
                    plain_values.append(value.rstrip())
                    if index == 0:
                        decimals = value.rstrip()[value.find("."):]
                        digits = len(decimals)-1
                resistance.append(clean_values[0])
                strengths.append(clean_values[1]/1000)
                strengths_uncerts.append(uncert_amp(plain_values[1])/1000)
                voltages.append(clean_values[2]*clean_values[3])
                voltages_uncerts.append(uncert_voltage(clean_values[3]))

        data = np.array([voltages,voltages_uncerts,strengths,strengths_uncerts,resistance])
        sorted_data = data[:, data[2].argsort()]

        file_string += titles[number] + " " + labels[n] + "\n"
        for i,e in enumerate(strengths):
            file_string += "Spannung: (%f +/- %f) V, Stromstärke: (%f +/- %f) A, %f Ohm\n" % (sorted_data[0][i],sorted_data[1][i],sorted_data[2][i],sorted_data[3][i],sorted_data[4][i])

        #plt.plot(sorted_data[0],sorted_data[2], marker='o',color=colors[n], linestyle="dotted", alpha=0.2, label=labels[n])
        plt.errorbar(sorted_data[2],sorted_data[0],yerr=sorted_data[1],xerr=sorted_data[3],color=colors[n], marker='x', linestyle="none", label=labels[n], markersize=2, markeredgewidth=0.5, capsize=3, linewidth=0.5)
        plt.xlabel("Stromstärke in A")
        plt.ylabel("Spannung in V")
        if(n==0):
            x = sorted_data[2]
            xerr = sorted_data[3]
            y = sorted_data[0]
            yerr = sorted_data[1]
            regression = perform_odr(x, y, xerr, yerr)
            regression_inv = perform_odr(y, x, yerr, xerr)
            plt.plot(x, linear_func(regression.beta,x), alpha=0.25, color='blue', linewidth="0.5", label="Lineare Regressionsgerade")
            plt.plot([], [], ' ', label="$a \\ = \\ %f$\n$u_a \\ = \\ %f$\n$b \\ = \\ %f$\n$u_b \\ = \\ %f$\n$\\chi^2 \\ = \\ %f$\n$x_0 = %f$\n$u_{x0} = %f$" % (regression.beta[0],regression.sd_beta[0],regression.beta[1],regression.sd_beta[1],regression.res_var,regression_inv.beta[1],regression_inv.sd_beta[1]))
            
            wattage = np.multiply(x,y)
            max_i = np.argmax(wattage)
            watt = max(wattage)
            res = sorted_data[4][max_i]

            print("[LKS] Maximale Leistung: %f, Lastwiderstand: %f" % (watt,res))
    plt.legend()
    plt.grid(linestyle='dotted')
    plt.savefig("Data" + str(number) + "_lks.png")
    plt.show()

text_file = open("lks_data.txt", "w")
n = text_file.write(file_string)
text_file.close()
print(file_string)