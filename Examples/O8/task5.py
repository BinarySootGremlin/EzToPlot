import matplotlib.pyplot as plt
import EzToPlot as ez
import math
import numpy as np
import scipy.special as sp
def formular(y,w):
    return y/10*w

def propagation(y,w,u_y,u_w):
    first_term = u_y/10*w
    second_term = u_w*y/10
    return math.sqrt(first_term**2+second_term**2)

def get_diameter():
    diam_file = open("aperature_diameter.ini","r")
    value = float(diam_file.readline().rstrip())
    sec = 1.003*10**(-2)
    u_sec = 0.003*10**(-2)
    return [(value*sec)*10**(-3),(value*u_sec)*10**(-3)]

def get_distance():
    dist_file = open("distance.ini","r")
    value = float(dist_file.readline().rstrip()) 
    return [value,20]

def get_wavelength():
    wavelength_file = open("wavelength.ini","r")
    value = float(wavelength_file.readline().rstrip())*10**(-9)
    return [value,0]

class statics:
    def __init__(self):
        self.B = 0
        self.L = 0
        self.W = 0

def bessel_func(p, x):
    a, b, c, d  = p

    B = statics.B
    L = statics.L
    W = statics.W
    x = c*x-d
    sinus_x = np.divide(x,np.sqrt(np.power(x,2)+np.power(L,2)))
    theta = np.divide(np.multiply(2*math.pi*B,sinus_x),W)
    bessel = sp.jv(1, np.divide(theta,2))
    denominator = np.divide(theta,4)
    inner = np.divide(bessel,denominator)
    output = a*np.power(inner,2)+b
#    for i,val in enumerate(x):
#        print("X: %f, sin(a): %f, theta: %f, bessel: %f, I: %f" % (val,sinus_x[i],theta[i],bessel[i],np.power(inner[i],2)))

    return output

def get_aperture_diameter(a,l,d,u_a,u_l,u_d):
    diam = a*l*d
    u_diam = np.sqrt((u_a*l*d)**2+(u_l*a*d)**2+(u_d*a*l)**2)
    return [diam,u_diam]

plotter = ez.ez_parser()
filename = "task5.ini"
plotter.setup_file(filename,0,1,y_settings_columns=[2],x_err_types=["plain"],y_err_types=["resolution","plain"],x_err_setting=[0.000005],y_err_setting=[1.5,0.1])
plotter.redefine_y(filename,filename,2,formular,propagation,uncert_types=["plain"],uncert_settings=[0])
plotter.shift_y(filename,0.000001)
#plotter.err_plot(filename,show=False)
plotter.file_parsers[filename].x_data.pop(0)
plotter.file_parsers[filename].y_data.pop(0)
plotter.file_parsers[filename].x_err.pop(0)
plotter.file_parsers[filename].y_err.pop(0)

#feed statics:
statics.B = get_diameter()[0]
statics.L = get_distance()[0]
statics.W = get_wavelength()[0]

plotter.fit_plot(filename,bessel_func,4,colors=["r"],override_start=[[1,1,1,0]],x_label="Verschiebung in m",y_label="Stromstärke\n in A",show=False)
plotter.describe("m","A")
#x = np.linspace(min(plotter.file_parsers[filename].x_data),max(plotter.file_parsers[filename].x_data),500)
#plt.plot(x,bessel_func([0.95,166.9,0.001],x))
plt.yscale('log')
plt.gcf().set_dpi(280)
plt.gcf().subplots_adjust(bottom=0.15)
plt.gcf().subplots_adjust(left=0.2)
plt.show()

#print(plotter.reduce(get_diameter()[0],get_diameter()[1]))

'''diam, u_diam = get_aperture_diameter(plotter.fit_values[0],get_wavelength()[0],get_distance()[0],plotter.fit_uncerts[0],get_wavelength()[1],get_distance()[1])
output = plotter.reduce(diam,u_diam)
print("Berechneter Durchmesser: (" + output[0] + " +/- " + output[1] + ") m")'''