import matplotlib.pyplot as plt
import EzToPlot as ez
import numpy as np
g = 9.81

def inv_length(l):
    return 1/l

def prop_length(l,u):
    if u == 0:
        return 0
    return np.sqrt((-u/l**2)**2)

def fit_func(p,x):
    a=p
    return a*x

def F0_minus_FH(k,m):
    return k*m*g

def prop_F0(k,m,u_k,u_m):
    first_term = u_k*m*g
    second_term = k*u_m*g
    return np.sqrt((first_term**2)+(second_term**2))

def freq_square(x,y):
    return x*(y*2)

def prop_square(x,y,u_x,u_y):
    first_term = u_x*(y*2)
    second_term = u_y*x*2
    return np.sqrt((first_term**2)+(second_term**2))

def freq_force(p,x):
    a,b=p
    return a*(b+x)

filename_1 = ["lks_task01.ini","jns_task01.ini"]
filename_2 = ["lks_task02.ini","jns_task02.ini"]
filename_3 = ["lks_task03.ini","jns_task03.ini"]
plotter = ez.ez_parser()

for i,e in enumerate(filename_1):
    #task1
    plotter.setup_file(filename_1[i],-1,0,y_err_types=["percentage","digit"],y_err_setting=[0.01,2])
    plotter.offset_x(filename_1[i],1)
    plotter.stretch_y(filename_1[i],2)
    #task2
    plotter.setup_file(filename_2[i],0,1,x_err_types=["plain"],x_err_setting=[0.5],y_err_types=["percentage","digit"],y_err_setting=[0.01,2])
    plotter.stretch_x(filename_2[i],0.01)
    plotter.modify_x(filename_2[i],inv_length,prop_length)
    plotter.stretch_y(filename_2[i],2)
    #task3
    plotter.setup_file(filename_3[i],1,0,y_err_types=["percentage","digit"],y_err_setting=[0.01,2])
    plotter.redefine_x(filename_3[i],filename_3[i],2,F0_minus_FH,prop_F0,uncert_types=["plain"],uncert_settings=[0.000005])
    plotter.file_parsers[filename_3[i]].x_err = plotter.file_parsers[filename_3[i]].x_err + np.divide(np.multiply(plotter.file_parsers[filename_3[i]].x_data,3),100)
    plotter.stretch_y(filename_3[i],2)
    plotter.redefine_y(filename_3[i],filename_3[i],0,freq_square,prop_square,uncert_types=["percentage","digit"],uncert_settings=[0.01,2])
plotter.fit_plot(filename_1,[fit_func,fit_func],[1,1],override_start=[[1],[1]],colors=["r","b"],legends_fit=["Fit Funktion xxx", "Fit Funktion yyy"],title="Messung #1",x_label="Schwingungsmode", y_label="Doppelte Erregerfrequenz in Hz")
plotter.fit_plot(filename_2,[fit_func,fit_func],[1,1],override_start=[[1],[1]],colors=["r","b"],legends_fit=["Fit Funktion xxx", "Fit Funktion yyy"],title="Messung #2",x_label="$\\frac{1}{l} \\ in \\ \\mathrm{m}^{-1}$", y_label="Doppelte Erregerfrequenz in Hz")
plotter.fit_plot(filename_3[1],[freq_force],[2],override_start=[[1,0]],colors=["b"],legends_fit=["Fit Funktion yyy"],title="Messung #3", x_label="$k\\cdot m\\cdot g \\ in \\ N$", y_label="$(2\\cdot f)^2$ in Hz$^2$",show=False)
plt.errorbar(plotter.file_parsers[filename_3[0]].x_data,plotter.file_parsers[filename_3[0]].y_data,xerr=plotter.file_parsers[filename_3[0]].x_err,yerr=plotter.file_parsers[filename_3[0]].y_err,label="Messdaten xxx",
                                marker='x', linestyle="none", markersize=2, markeredgewidth=0.5, capsize=3, linewidth=0.5, color="r")
plt.legend()
plt.show()

plotter.describe()
#TEST
#plotter.setup_file("lks_task031.ini",1,0,y_err_types=["percentage","digit"],y_err_setting=[0.01,2])
#plotter.redefine_x("lks_task031.ini","lks_task031.ini",2,F0_minus_FH,prop_F0,uncert_types=["plain"],uncert_settings=[0.000005])
#plotter.stretch_y("lks_task031.ini",2)

#plotter.setup_file("lks_task032.ini",1,0,y_err_types=["percentage","digit"],y_err_setting=[0.01,2])
#plotter.redefine_x("lks_task032.ini","lks_task032.ini",2,F0_minus_FH,prop_F0,uncert_types=["plain"],uncert_settings=[0.000005])
#plotter.stretch_y("lks_task032.ini",2)

#plotter.fit_plot([filename_3[0],"lks_task031.ini","lks_task032.ini"],[freq_force,freq_force,freq_force],[2,2,2],override_start=[[1,0],[1,0],[1,0]],colors=["r","g","b"],legends_fit=["Fit Funktion Kerbe 5","Fit Funktion Kerbe 1","Fit Funktion Kerbe 3"],title="Messung #3", x_label="$\\sqrt{k\\cdot m\\cdot g} \ in \ \\mathrm{N}$", y_label="Doppelte \n Erregerfrequenz \n in Hz")