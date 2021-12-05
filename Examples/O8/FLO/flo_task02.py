import numpy as np
import EzToPlot as ez
import matplotlib.pyplot as plt
import matplotlib as mpl

def linear_func(p, x):  
   a = p  
   return np.multiply(a,x)

def get_distance():
    dist_file = open("flo_distance02.ini","r")
    value = float(dist_file.readline().rstrip()) 
    return [value,0.02]

def get_wavelength():
    wavelength_file = open("../wavelength.ini","r")
    value = float(wavelength_file.readline().rstrip())*10**(-9)
    return [value,0]

def get_width(d, l, a, u_d, u_l, u_a):
    b = d*l/a
    u_b = np.sqrt((u_d*l/a)**2+(d*u_l/a)**2+(-d*l*u_a/a**2)**2)
    return [b,u_b]

filename = "flo_task02.ini"
plotter = ez.ez_parser()
plotter.setup_file(filename,x_column=0,y_column=1,y_err_types=["plain","percentage"],y_err_setting=[0.07,1])
plotter.shift_y(filename,0.005)
plotter.describe()
#plotter.err_plot("test_values.ini","Messung","Beugungsordnung","Abstand")

plotter.fit_plot(filename, linear_func, 1, colors=["r"],override_start=[[1]],legends_fit=["Fitfunktion"],title="$Messung_{flo}$",x_label="Beugungsminimum #",y_label="Abstand zur\n 0. Ordnung\n in m",show=False)
plt.ylim(0, 0.04)
plt.xlim(0, 11)
plt.gcf().set_dpi(280)
plt.gcf().subplots_adjust(bottom=0.15)
plt.gcf().subplots_adjust(left=0.2)
plt.show()

d, u_d = get_distance()
l, u_l = get_wavelength()
width, u_width = get_width(d,l,plotter.fit_values[0],u_d,u_l,plotter.fit_uncerts[0])
output = plotter.reduce(width,u_width)
print("Spaltbreite: (" + output[0] + " +/- " + output[1] + ") m")