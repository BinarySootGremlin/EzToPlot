import matplotlib.pyplot as plt
import EzToPlot as ez
import math
import numpy as np

def degtorad(x):
    return math.pi*x/180

def calc_R(x,u):
    return math.sqrt(x/u)

def gauss_propagation(x,u,u_x,u_u):
    first_term = math.sqrt(x/u)/(2*x)*u_x
    second_term = -math.sqrt(x/u)/(2*u)*u_u
    return math.sqrt(first_term**2+second_term**2)

def RS(p, x):  
   a = p  
   x = np.deg2rad(x)
   return np.sqrt(np.power(np.sin(np.arcsin(a*np.sin(x))-x),2)/np.power(np.sin(x+np.arcsin(a*np.sin(x))),2))

def RP(p, x):
    a,b = p
    x = np.deg2rad(x)
    return np.sqrt(np.power(np.tan(np.arcsin(a*np.sin(x))-x),2)/np.power(np.tan(x+np.arcsin(a*np.sin(x))),2)) + b

plotter = ez.ez_parser()
plotter.setup_file("flo_normal.ini",x_column=0,y_column=1,y_err_types=["percentage","digit"],y_err_setting=[1.5,10],x_err_types=["plain"],x_err_setting=[2])
plotter.setup_file("flo_parallel.ini",x_column=0,y_column=1,y_err_types=["percentage","digit"],y_err_setting=[1.5,10],x_err_types=["plain"],x_err_setting=[2])
plotter.redefine_y("flo_normal.ini","flo_normal_u0.ini",0,calc_R,gauss_propagation,uncert_types=["percentage","digit"],uncert_settings=[1.5,10])
plotter.redefine_y("flo_parallel.ini","flo_parallel_u0.ini",0,calc_R,gauss_propagation,uncert_types=["percentage","digit"],uncert_settings=[1.5,10])

#plotter.err_plot(["flo_normal.ini","flo_parallel.ini"],y_label="$\\sqrt{\\frac{U_{\\alpha}}{U_0}}$",x_label="$\\alpha \\ in \\ °$")
plotter.fit_plot(["flo_normal.ini","flo_parallel.ini"],[RS,RP],[1,2],["r","b"],override_start=[[0.1],[0.5,0.5]],
                legends_fit=["Senkrechte Polarisation - Fitfunktion","Parallele Polarisation - Fitfunktion"],
                x_label="$\\alpha \\ in \\ °$", y_label="$\\sqrt{\\frac{U_r(\\alpha)}{U_0}}$", title="$Messergebnisse \\ und \\ Regression_{flo}$",show=False)
plotter.describe()
x = np.linspace(10,80,500)
#plt.plot(x,RS(1/1.492,x),color="maroon",label="Theoretischer Verlauf (Senkrecht)")
#plt.plot(x,RP([1/1.492,0],x),color="navy",label="Theoretischer Verlauf (Parallel)")
plt.legend()
plt.show()