import math
def val(x,b,c):
    return (x+b)/(c)**2

def prop(x,b,c,u_x,u_b,u_c):
    first_term = u_x/c**2
    second_term = u_b/c**2
    third_term = -(2*(b+x)/c**3)*u_c
    return math.sqrt(first_term**2+second_term**2+third_term**2)

b_ctrans1 = 192.6
u_bc1 = 1.7

h_ctrans1 = 198.0
u_hc1 = 1.9


b_ctrans2 = 191.94
u_bc2 = 0.2

h_ctrans2 = 197.3
u_hc2 = 0.14

b = 0.49
u_b = 0.2

x1 = 3*9.81
u_x1 = 0.005*5*9.81*3

x2 = 3*9.81
u_x2 = 0.005*5*9.81*3

b_m1 = val(x1,b,b_ctrans1)*1000
u_bm1 = prop(x1,b,b_ctrans1,u_x1,u_b,u_bc1)*1000
b_m2 = val(x1,b,b_ctrans2)*1000
u_bm2 = prop(x2,b,b_ctrans2,u_x2,u_b,u_bc2)*1000

h_m1 = val(x1,b,h_ctrans1)*1000
u_hm1 = prop(x1,b,h_ctrans1,u_x1,u_b,u_hc1)*1000
h_m2 = val(x1,b,h_ctrans2)*1000
u_hm2 = prop(x2,b,h_ctrans2,u_x2,u_b,u_hc2)*1000

print("#1 B: %f +- %f C: %f +- %f" % (b_m1,u_bm1,h_m1,u_hm1))
print("#2 B: %f +- %f C: %f +- %f" % (b_m2,u_bm2,h_m2,u_hm2))