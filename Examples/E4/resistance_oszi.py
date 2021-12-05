import numpy as np

def gauss_uncert(R_P,U_GEN,U_P,U_RP,U_UGEN,U_UP):
    first_term = (U_GEN/U_P)-1
    second_term = R_P/U_P
    third_term = -(R_P*U_GEN)/U_P**2
    return np.sqrt((first_term*U_RP)**2+(second_term*U_UGEN)**2+(third_term*U_UP)**2)

def gauss_uncert_i(U_P,R_P,U_UP,U_RP):
    first_term = 1/R_P
    second_term = -U_P/R_P**2
    return np.sqrt((first_term*U_UP)**2+(second_term*U_RP)**2)

data = [[10,6.486,0.2341,0.5,0.072430,0.005170],[10,6.384,0.2326,0.5,0.071920,0.005163]]

for i,e in enumerate(data):
    R_P = e[0]
    U_GEN = e[1]
    U_P = e[2]
    R_X = R_P*((U_GEN/U_P) - 1)
    U_RX = gauss_uncert(e[0],e[1],e[2],e[3],e[4],e[5])
    I = U_P/R_P
    U_I = gauss_uncert_i(U_P,R_P,e[5],e[3])
    if i == 0:
        print("xxx : I: (%f +/- %f) R_X: (%f +/- %f)" % (I, U_I, R_X, U_RX))
    else:
        print("yyy I: (%f +/- %f) R_X: (%f +/- %f)" % (I, U_I, R_X, U_RX))