import math

def val(a,l):
    return a*2*l

def uncert(a,l,u_a,u_l):
    first_term = u_a*2*l
    second_term = u_l*2*a
    return math.sqrt(first_term**2+second_term**2)

b_a = 160.51
b_ua = 0.31
h_a = 165.0
h_ua = 0.8

l = 0.6
u_l = 0.005

b_c = [val(b_a,l),uncert(b_a,l,b_ua,u_l)]
h_c = [val(h_a,l),uncert(h_a,l,h_ua,u_l)]

print(b_c)
print("----------")
print(h_c)