import matplotlib.pyplot as plt
import EzToPlot as ez
import numpy as np

quad_len = 0.08
u_quad_len = 0.0005

k = 0.00211571
u_k = 0.0001

d = 8*10**(-3)
u_d = 0

def KI(data):
    output = 0.0
    output = sigma(data)/np.sqrt(len(data))
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
        output += np.square(x_i-my(data))
    output /= (len(data)-1)
    output = np.sqrt(output)
    return output

def inv_x(x):
    return 1/x

def inv_prop(x,u_x):
    return np.sqrt((-u_x/x**2)**2)

def radius(x):
    return (quad_len**2+x**2)/(np.sqrt(2)*(quad_len-x))

def radius_prop(x,u_x):
    first_term = (quad_len**2+2*quad_len*x-x**2)/(np.sqrt(2)*(quad_len-x)**2)*u_x
    second_term = (quad_len**2-2*quad_len*x-x**2)/(np.sqrt(2)*(quad_len-x)**2)*u_quad_len
    return np.sqrt(first_term**2+second_term**2)

def linear(p,x):
    a,b=p
    return a*x+b

def linear_simple(p,x):
    a=p
    return a*x

def get_specific_charge_01(a,U,k,u_a,u_U,u_k):
    spec_charge = 2*U/((a**2)*(k**2))
    first_term = -4*U/((a**3)*(k**2))*u_a
    second_term = 2*((a**2)*(k**2))*u_U
    third_term = -4*U/((a**2)*(k**3))*u_k
    return [spec_charge,np.sqrt(first_term**2+second_term**2+third_term**2)]

def get_specific_charge_02(a,U,d,k,u_a,u_U,u_d,u_k):
    spec_charge = (a**2)/(2*U*(d**2)*(k**2))
    first_term = a/(2*U*(d**2)*(k**2))*u_a
    second_term = -(a**2)/(2*(d**2)*(k**2)*(U**2))*u_U
    third_term = -(a**2)/((k**2)*U*(d**3))*u_d
    fourth_term = -(a**2)/((d**2)*(k**3)*U)*u_k
    return [spec_charge,np.sqrt((first_term**2)+(second_term**2)+(third_term**2)+(fourth_term**2))]

def magnet_fit(p,x):
    a,b = p
    my = 4*np.pi*10**(-7)
    I=540
    R=0.136/2
    N=320
    w = x-a
    return my*N*b/(4*R)*((1+(w/R+1/2)**2)**(-3/2)+(1+(w/R-1/2)**2)**(-3/2))

plotter = ez.ez_parser()

magnet_filename01 = "magnet01.ini"
plotter.setup_file(magnet_filename01,0,1,x_err_types=["plain"],x_err_setting=[0.5],y_err_types=["percentage"],y_err_setting=[2])
plotter.offset_x(magnet_filename01,-3)
plotter.stretch_x(magnet_filename01,0.01)
plotter.stretch_y(magnet_filename01,0.001)
#plotter.err_plot(magnet_filename01,"Radiale Feldverteilung in der Helmholtzspule","Verschiebung in m","Magnetfeldstärke in mT",legends=["Messpunkte"],show=False)
plotter.fit_plot(magnet_filename01,magnet_fit,2,colors=["r"],override_start=[[0,600]],x_label="Versatz in m",y_label="Magnetfeldstärke in T",param_names=["x-offset","I_B","Skalierung_R"],x_lim=[0,0.14])
plotter.describe()
'''my = 4*np.pi*10**(-7)
I=0.678867
R=0.136/2
N=320
x = np.linspace(np.min(plotter.file_parsers[magnet_filename01].x_data),np.max(plotter.file_parsers[magnet_filename01].x_data),200)
offset = R
y = my*N*I/(4*R)*((1+((x-offset)/R+1/2)**2)**(-3/2)+(1+((x-offset)/R-1/2)**2)**(-3/2))-0.0003
plt.plot(x,y,label="Theoretischer Verlauf")
plt.legend()
plt.show()'''

magnet_filename02 = "magnet02.ini"
plotter.setup_file(magnet_filename02,0,1,x_err_types=["percentage","digit"],x_err_setting=[1.5,5],y_err_types=["percentage","plain"],y_err_setting=[2,0.00000001])
plotter.stretch_y(magnet_filename02,0.001)
plotter.fit_plot(magnet_filename02,linear_simple,[1],["r"],title="Messung Magnetfeldstärke",x_label="Stromstärke in A",y_label="Magnetfeldstärke in mT",param_names=["k"])

filenames_01 = [["jns_task01_3.ini","jns_task01_4.ini","jns_task01_5.ini"],["lks_task01_3.ini","lks_task01_4.ini","lks_task01_5.ini"],["flo_task01_3.ini","flo_task01_4.ini","flo_task01_5.ini"]]
names = ["JNS","LKS","FLO"]
U = [3000,4000,5000]
u_U = 5000/100*2.5
first_data = []
for count, filenames in enumerate(filenames_01):
    print(filenames[0])
    plotter.setup_file(filenames[0],0,1,y_err_types=["add"],y_settings_columns=[2],x_err_types=["percentage","digit"],x_err_setting=[1.5,5])
    plotter.modify_x(filenames[0],inv_x,inv_prop)
    plotter.stretch_y(filenames[0],0.002)
    plotter.modify_y(filenames[0],radius,radius_prop)

    plotter.setup_file(filenames[1],0,1,y_err_types=["plain"],y_err_setting=[0.5],x_err_types=["percentage","digit"],x_err_setting=[1.5,5])
    plotter.modify_x(filenames[1],inv_x,inv_prop)
    plotter.stretch_y(filenames[1],0.002)
    plotter.modify_y(filenames[1],radius,radius_prop)

    plotter.setup_file(filenames[2],0,1,y_err_types=["plain"],y_err_setting=[0.5],x_err_types=["percentage","digit"],x_err_setting=[1.5,5])
    plotter.modify_x(filenames[2],inv_x,inv_prop)
    plotter.stretch_y(filenames[2],0.002)
    plotter.modify_y(filenames[2],radius,radius_prop)

    plotter.fit_plot([filenames[0],filenames[1],filenames[2]],[linear,linear,linear],[2,2,2],["r","g","b"],names[count],override_start=[[1,0],[1,0],[1,0]],x_label="$\\frac{1}{I} \\ in \\ \\mathrm{A}^{-1} $",y_label="$r(I)$",legends_fit=["3kV","4kV","5kV"],param_names=["Steigung","y-offset"])
    
    specific_charges = []

    for i in range(3):
        a = plotter.file_parsers[filenames[i]].get_fit_params()[0]
        u_a = plotter.file_parsers[filenames[i]].get_fit_params_uncerts()[0]
        output = get_specific_charge_01(a,U[i],k,u_a,u_U,u_k)
        out_str = plotter.reduce(output[0],output[1])
        print("e/m #%d: (%s +/- %s) C/kg" % (i,out_str[0],out_str[1]))
        specific_charges.append(output[0])

    print("Mittel: %f, Standardabweichung: %f, Vertrauensbereich: %f" % (my(specific_charges),sigma(specific_charges),KI(specific_charges)))
    first_data.append(my(specific_charges))
second_data = []
filenames_02 = [["jns_task02_3.ini","jns_task02_4.ini","jns_task02_5.ini"],["lks_task02_3.ini","lks_task02_4.ini","lks_task02_5.ini"],["flo_task02_3.ini","flo_task02_4.ini","flo_task02_5.ini"]]
print("---------------------")
for count, filenames in enumerate(filenames_02):
    print(filenames[0])
    plotter.setup_file(filenames[0],0,1,y_err_types=["plain"],y_err_setting=[10],x_err_types=["percentage","digit"],x_err_setting=[1.5,5])

    plotter.setup_file(filenames[1],0,1,y_err_types=["plain"],y_err_setting=[10],x_err_types=["percentage","digit"],x_err_setting=[1.5,5])

    plotter.setup_file(filenames[2],0,1,y_err_types=["plain"],y_err_setting=[25],x_err_types=["percentage","digit"],x_err_setting=[1.5,5])

    plotter.fit_plot([filenames[0],filenames[1],filenames[2]],[linear,linear,linear],[2,2,2],override_start=[[1,0],[1,0],[1,0]],colors=["r","g","b"],x_label="$\\mathrm{I \\ in \\ A}$",y_label="$U_K(I) \\ in \\ \\mathrm{V}$",legends_fit=["3kV","4kV","5kV"],title=names[count],param_names=["Steigung","y-offset"])

    specific_charges = []

    for i in range(3):
        a = plotter.file_parsers[filenames[i]].get_fit_params()[0]
        u_a = plotter.file_parsers[filenames[i]].get_fit_params_uncerts()[0]
        output = get_specific_charge_02(a,U[i],d,k,u_a,u_U,u_d,u_k)
        out_str = plotter.reduce(output[0],output[1])
        print("e/m #%d: (%s +/- %s) C/kg" % (i,out_str[0],out_str[1]))
        specific_charges.append(output[0])

    print("Mittel: %f, Standardabweichung: %f, Vertrauensbereich: %f" % (my(specific_charges),sigma(specific_charges),KI(specific_charges)))
    second_data.append(my(specific_charges))
print("#1: Mittel: %f, Standardabweichung: %f, Vertrauensbereich: %f" % (my(first_data),sigma(first_data),KI(first_data)))
print("#2: Mittel: %f, Standardabweichung: %f, Vertrauensbereich: %f" % (my(second_data),sigma(second_data),KI(second_data)))
#plotter.describe()