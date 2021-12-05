import numpy as np

def gauss_uncert(L,C,U_L,U_C):
    first_term = -C/(4*np.pi*np.sqrt((L*C)**3))
    second_term = -L/(4*np.pi*np.sqrt((L*C)**3))
    return np.sqrt((first_term*U_L)**2+(second_term*U_C)**2)

C = [0.0000000924,0.000000113]
U_C = [0.000000324,0.000000410]

L = [0.510078,0.498459]
U_L = [0.128677,0.139478]

#0:xxx,1:yyy
f_res = []

for i,e in enumerate(C):
    f_res += [1/(2*np.pi*np.sqrt(L[i]*C[i])),gauss_uncert(L[i],C[i],U_L[i],U_C[i])]

print("[xxx]: Resonanz-Frequenz: (%f +/- %f)" % (f_res[0], f_res[1]))
print("[yyy]: Resonanz-Frequenz: (%f +/- %f)" % (f_res[2], f_res[3]))