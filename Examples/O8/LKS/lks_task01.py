import numpy as np
import EzToPlot as ez
import matplotlib.pyplot as plt

def linear_func(p, x):  
   a,b = p  
   return np.multiply(a,x)+b

def get_distance():
    dist_file = open("lks_distance01.ini","r")
    value = float(dist_file.readline().rstrip()) 
    return [value,0.02]

def get_wavelength():
    wavelength_file = open("../wavelength.ini","r")
    value = float(wavelength_file.readline().rstrip())*10**(-9)
    return [value,0]

def get_constant(d, l, a, u_d, u_l, u_a):
    b = d*l/a
    u_b = np.sqrt((u_d*l/a)**2+(d*u_l/a)**2+(-d*l*u_a/a**2)**2)
    return [b,u_b]

filename = "lks_task01.ini"
plotter = ez.ez_parser()
plotter.setup_file(filename,x_column=0,y_column=1,y_err_types=["plain","percentage"],y_err_setting=[0.0007,1])
plotter.describe()
#plotter.err_plot("test_values.ini","Messung","Beugungsordnung","Abstand")

plotter.fit_plot(filename, linear_func, 2, colors=["r"],override_start=[[1,0]],title="$Messung_{lks}$",x_label="Beugungsmaximum #",y_label="Abstand zur\n 0. Ordnung\n in m",show=False)
plt.ylim(0, 0.3)
plt.xlim(0, 6)
plt.gcf().set_dpi(280)
plt.gcf().subplots_adjust(bottom=0.15)
plt.gcf().subplots_adjust(left=0.2)
plt.show()

d, u_d = get_distance()
l, u_l = get_wavelength()
constant, u_constant = get_constant(d,l,plotter.fit_values[0],u_d,u_l,plotter.fit_uncerts[0])
output = plotter.reduce(constant,u_constant)
print("Gitterkonstante: (" + output[0] + " +/- " + output[1] + ") m")