import matplotlib.pyplot as plt
from matplotlib import cycler
import matplotlib as mpl
import numpy as np

def linRegDeterminant(x,y,s):
    x = np.asarray(x)
    y = np.asarray(y)
    s = np.asarray(s)
    D = np.sum(np.power(x/s,2))*np.sum(np.power(1/s,2))-np.power(np.sum(x/np.power(s,2)),2)
    return D

def linRegSlope(x,y,s,D):
    x = np.asarray(x)
    y = np.asarray(y)
    s = np.asarray(s)
    a = 1/D*(np.sum(x*y/(s*s))*np.sum(1/(s*s))-np.sum(x/(s*s))*np.sum(y/(s*s)))
    return a

def linRegIntersect(x,y,s,D):
    x = np.asarray(x)
    y = np.asarray(y)
    s = np.asarray(s)
    b = 1/D*(np.sum(x*x/(s*s))*np.sum(y/(s*s))-np.sum(x*y/(s*s))*np.sum(x/(s*s)))
    return b

def linRegUncertaintyCoef(s,D):
    s = np.asarray(s)
    sa = np.sqrt(1/D*np.sum(1/(s*s)))
    return sa

def linRegUncertaintyIntersect(x,s,D):
    x = np.asarray(x)
    s = np.asarray(s)
    sb = np.sqrt(1/D*np.sum(x*x/(s*s)))
    return sb

def linRegCorrelationCoeff(x,y):
    x = np.asarray(x)
    y = np.asarray(y)
    xdiv = (x-np.mean(x))
    ydiv = (y-np.mean(y))
    r = np.sum(xdiv*ydiv)/np.sqrt(np.sum(np.square(xdiv))*np.sum(np.square(ydiv)))
    return r

def linRegRsquared(r):
    return r*r

def linRegChisquared(x,y,s,Slope,Intersect):
    x = np.asarray(x)
    y = np.asarray(y)
    Expected = Slope * x + Intersect
    Chi = np.sum(np.square((y-Expected)/s))
    return Chi

def linRegForceOriginSlope(x,y,s):
    x = np.asarray(x)
    y = np.asarray(y)
    s = np.asarray(s)
    a = np.sum(x*y/(s*s))/np.sum(x*x/(s*s))
    return a

def linRegForceOriginSlopeError(x,s):
    x = np.asarray(x)
    s = np.asarray(s)
    sa = np.sqrt(1/np.sum(x*x/(s*s)))
    return sa

class LinearReg:
    def __init__(self,x,y,s):
        self.x = x
        self.y = y
        self.s = s
        self.Det = linRegDeterminant(x,y,s)
        self.Slope = linRegSlope(x,y,s,self.Det)
        self.Intersect = linRegIntersect(x,y,s,self.Det)
        self.SlopeError = linRegUncertaintyCoef(s,self.Det)
        self.IntersectError = linRegUncertaintyIntersect(x,s,self.Det)
        self.CorrelationCoef = linRegCorrelationCoeff(x,y)
        self.Rsquared = linRegRsquared(self.CorrelationCoef)
        self.Chisquared = linRegChisquared(self.x,self.y,self.s,self.Slope,self.Intersect)
        self.Origin = False
    
    def forceOrigin(self,t):
        if(t != self.Origin):
            self.Origin = t
            if(t == True):
                self.Slope = linRegForceOriginSlope(self.x,self.y,self.s)
                self.SlopeError = linRegForceOriginSlopeError(self.x,self.s)
                self.Chisquared = linRegChisquared(self.x,self.y,self.s,self.Slope,self.Intersect)
                self.Intersect = 0
                self.IntersectError = 0
            else:
                self.Slope = linRegSlope(self.x,self.y,self.s,self.Det)
                self.SlopeError = linRegUncertaintyCoef(self.s,self.Det)
                self.Intersect = linRegIntersect(self.x,self.y,self.s,self.Det)
                self.IntersectError = linRegUncertaintyIntersect(self.x,self.s,self.Det)
                self.Chisquared = linRegChisquared(self.x,self.y,self.s,self.Slope,self.Intersect)
    def describe(self):
        print("R^2 = "+str(self.Rsquared) + "\n"+"Chi^2 = "+str(self.Chisquared)+"\n"+"a = "+str(self.Slope)+"\n"+"ua = "+str(self.SlopeError)+"\n"+"b = "+str(self.Intersect)+"\n"+"ub = "+str(self.IntersectError))

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

def gauss_uncert(U_c1, U_c2, R_P, U_c1_uncert, U_c2_uncert, r_p_uncert):
    U_c1_deriv = R_P/U_c2
    U_c2_deriv = -(R_P*U_c1)/(U_c2**2)
    R_P_deriv = (U_c1-U_c2)/U_c2 
    return np.sqrt((U_c1_deriv*U_c1_uncert)**2+(U_c2_deriv*U_c2_uncert)**2+(R_P_deriv*r_p_uncert)**2)

def correct_freq_and_uncert(freq,additional_uncert = 0):
    return [freq,freq/100*5]

fig, axs = plt.subplots(2, 2)

filelist = [["dataset01_lks.ini", "dataset02_lks.ini"],["dataset01_flo.ini","dataset02_flo.ini"]]

axs[0,0].set_title("Messergebnisse: xxx")
axs[0,1].set_title("Messergebnisse: yyy")
axs[0,0].annotate("Kondensator", xy=(0, 0.5), xytext=(-axs[0,0].yaxis.labelpad - 5, 0),
                xycoords=axs[0,0].yaxis.label, textcoords='offset points',
                size='large', ha='right', va='center')
axs[1,0].annotate("Spule", xy=(0, 0.5), xytext=(-axs[1,0].yaxis.labelpad - 5, 0),
                xycoords=axs[1,0].yaxis.label, textcoords='offset points',
                size='large', ha='right', va='center')
for index,files in enumerate(filelist):

    R_P = 10
    R_P_UNCERT = 0.5

    data_01 = []
    data_02 = []

    filename = files[0][files[0].rfind("\\")+1:]
    filename = filename[0:filename.find(".")]

    clean_values = []
    with open(files[0]) as f:
        for line in f:
            clean_values.clear()
            for value in line.split(","):
                clean_values.append(float(value.rstrip()))
            data_01.append(clean_values.copy())

    with open(files[1]) as f:
        for line in f:
            clean_values.clear()
            for value in line.split(","):
                clean_values.append(float(value.rstrip()))
            data_02.append(clean_values.copy())

    freqs01 = []
    freqs_uncert01 = []
    U_C101 = []
    U_C101_fact = []
    U_C201 = []
    U_C201_fact = []

    for entry in data_01:
        freqs_uncerts = correct_freq_and_uncert(entry[0]*1000)
        freqs01.append(1/freqs_uncerts[0]**2)
        freqs_uncert01.append((1/freqs_uncerts[0]**3)*freqs_uncerts[1])
        U_C101.append(entry[1])
        U_C101_fact.append(entry[2])
        U_C201.append(entry[3])
        U_C201_fact.append(entry[4])

    z1 = []
    z1_uncert = []
    for i,element in enumerate(U_C101):
        z1.append((R_P*(U_C101[i]-U_C201[i])/U_C201[i])**2)
        z1_uncert.append(2*(R_P*(U_C101[i]-U_C201[i])/U_C201[i])*gauss_uncert(U_C101[i],U_C201[i],R_P,U_C101_fact[i]*0.2,U_C201_fact[i]*0.2,R_P_UNCERT))

    axs[0][index].set(ylabel="$|Z|^2$", xlabel="$1/f^2$")

    obj = LinearReg(freqs01,z1,z1_uncert)

    # 20 linearly spaced numbers
    x_3 = np.linspace(np.min(freqs01),np.max(freqs01),20)

    axs[0][index].plot(x_3, obj.Slope*x_3 + obj.Intersect, alpha=0.25,color='blue',label="Fit")
    axs[0][index].errorbar(freqs01,z1,xerr=0,yerr=0,linestyle="none")
    C = 1/np.sqrt(obj.Slope*(4*np.pi**2))
    C_ERR = 1/np.sqrt(obj.SlopeError*(4*np.pi**2))
    if(index==0):
        print("xxx: [Kondensator] Kapazität: (%.2E +/- %.2E) Chi^2: %f" % (C,C_ERR,obj.Chisquared))
    else:
        print("yyy: [Kondensator] Kapazität: (%.2E +/- %.2E) Chi^2: %f" % (C,C_ERR,obj.Chisquared))

    freqs02 = []
    freqs_uncert02 = []
    U_C102 = []
    U_C102_fact = []
    U_C202 = []
    U_C202_fact = []

    for entry in data_02:
        freqs_uncerts = correct_freq_and_uncert(entry[0])
        freqs02.append(freqs_uncerts[0]**2)
        freqs_uncert02.append(2*freqs_uncerts[0]*freqs_uncerts[1])
        U_C102.append(entry[1])
        U_C102_fact.append(entry[2])
        U_C202.append(entry[3])
        U_C202_fact.append(entry[4])

    z2 = []
    z2_uncert =[]
    for i,element in enumerate(U_C102):
        z2.append((R_P*(U_C102[i]-U_C202[i])/U_C202[i])**2)
        z2_uncert.append(2*(R_P*(U_C102[i]-U_C202[i])/U_C202[i])*gauss_uncert(U_C102[i],U_C202[i],R_P,U_C102_fact[i]*0.2,U_C202_fact[i]*0.2,R_P_UNCERT))

    axs[1][index].set(ylabel="$|Z|^2$", xlabel="$f^2$")

    obj = LinearReg(freqs02,z2,z2_uncert)
    #obj.describe()

    # 20 linearly spaced numbers
    x_3 = np.linspace(np.min(freqs02),np.max(freqs02),20)
    axs[1][index].plot(x_3, obj.Slope*x_3 + obj.Intersect, alpha=0.25,color='blue',label="Fit")
    axs[1][index].errorbar(freqs02,z2,xerr=0,yerr=0,linestyle="none")
    if(index==0):
        print("Lukas: [Spule] Ohm'scher Widerstand: (%f +/- %f) Induktivität: (%f +/- %f), Chi^2: %f" % (np.sqrt(obj.Intersect),np.sqrt(obj.IntersectError),np.sqrt(obj.Slope/(4*np.pi**2)),np.sqrt(obj.SlopeError/(4*np.pi**2)),obj.Chisquared))
    else:
        print("Flo: [Spule] Ohm'scher Widerstand: (%f +/- %f) Induktivität: (%f +/- %f) Chi^2: %f" % (np.sqrt(obj.Intersect),np.sqrt(obj.IntersectError),np.sqrt(obj.Slope/(4*np.pi**2)),np.sqrt(obj.SlopeError/(4*np.pi**2)),obj.Chisquared))

top_left_max_y = axs[0][0].get_ylim()[1]
top_right_max_y = axs[0][1].get_ylim()[1]
bottom_left_max_y = axs[1][0].get_ylim()[1]
bottom_right_max_y = axs[1][1].get_ylim()[1]

max_top01_y = np.maximum(top_left_max_y,top_right_max_y)
max_top02_y = np.maximum(bottom_left_max_y,bottom_right_max_y)

axs[0][0].set_ylim(0,max_top01_y)
axs[0][1].set_ylim(0,max_top01_y)
axs[1][0].set_ylim(0,max_top02_y)
axs[1][1].set_ylim(0,max_top02_y)

top_left_max_x = axs[0][0].get_xlim()[1]
top_right_max_x = axs[0][1].get_xlim()[1]
bottom_left_max_x = axs[1][0].get_xlim()[1]
bottom_right_max_x = axs[1][1].get_xlim()[1]

max_top01_x = np.maximum(top_left_max_x,top_right_max_x)
max_top02_x = np.maximum(bottom_left_max_x,bottom_right_max_x)

axs[0][0].set_xlim(0,max_top01_x)
axs[0][1].set_xlim(0,max_top01_x)
axs[1][0].set_xlim(0,max_top02_x)
axs[1][1].set_xlim(0,max_top02_x)

plt.show()