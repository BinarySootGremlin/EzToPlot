import numpy as np 

def gauss_uncert_rho(U_SPULE,U_GEN,U_P,U_USPULE,U_UGEN,U_UP):
    first_term = 1/(U_GEN-U_P)
    second_term = -U_SPULE/(U_GEN-U_P)**2
    third_term = U_SPULE/(U_GEN-U_P)**2
    return np.sqrt((first_term*U_USPULE)**2+(second_term*U_UGEN)**2+(third_term*U_UP)**2)

def gauss_uncert_rs_rho(rho,RES,L,U_rho,U_RES,U_L):
    first_term = -2*np.pi*RES*L/rho**2
    second_term = 2*np.pi*L/rho
    third_term = 2*np.pi*RES/rho
    return np.sqrt((first_term*U_rho)**2+(second_term*U_RES)**2+(third_term*U_L)**2)

U_GEN = [6.486000,6.384000]
U_UGEN = [0.072430,0.071920]

U_SPULE = [53.620000,50.710000]
U_USPULE = [0.668100,0.653550]

U_P = [0.234100,0.232600]
U_UP = [0.005170,0.005163]

RES = [734.193333,683.383333]
U_RES = [0.201362,0.050067]

L = [0.508964,0.498193]
U_L = [0.025914,0.029066]

for i,e in enumerate(U_GEN):
    rho = U_SPULE[i]/(U_GEN[i]-U_P[i])
    rho_uncert = gauss_uncert_rho(U_SPULE[i],U_GEN[i],U_P[i],U_USPULE[i],U_UGEN[i],U_UP[i])
    if i == 0:
        print("xxx: rho: (%f +/- %f)" % (rho,rho_uncert))
    else:
        print("yyy: rho: (%f +/- %f)" % (rho,rho_uncert))

    r_s = 2*np.pi*RES[i]*L[i]/rho
    r_s_uncert = gauss_uncert_rs_rho(rho,RES[i],L[i],rho_uncert,U_RES[i],U_L[i])

    if i == 0:
        print("xxx: R_S: (%f +/- %f)" % (r_s,r_s_uncert))
    else:
        print("yyy: R_S: (%f +/- %f)" % (r_s,r_s_uncert))