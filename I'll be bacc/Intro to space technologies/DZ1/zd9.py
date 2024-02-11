import numpy as np
import math
from scipy.optimize import fsolve

mi = 398600
earth_radius = 6371.0 # km
time_elapsed = 194.0 # min
delta_t = time_elapsed * 60

r_vector = np.array([9095.5, 37423.9, 1350.0])
v_vector = np.array([-2.16, -0.35, 0.95])

# a)

r = np.linalg.norm(r_vector)
v = np.linalg.norm(v_vector)

v_r = np.dot(r_vector, v_vector) / r
print('v_r: {}'.format(v_r))

h_vector = np.cross(r_vector, v_vector)
h = np.linalg.norm(h_vector)
print("h = {} kg*km^2/s".format(h))
print("h_vect = {} km^3/s ".format(h_vector))

i = math.acos(h_vector[2] / h)
print("i = {} rad = {} deg".format(i, 360*i / (2*math.pi)))

e_vector = (1 / mi) * (np.cross(v_vector, h_vector) - mi * (r_vector / r))
e = np.linalg.norm(e_vector)
print('e: {}'.format(e))

k_vector = np.array([0, 0, 1])
N_vector = np.cross(k_vector, h_vector)
N = np.linalg.norm(N_vector)
print("N = {} ".format(N))

OMEGA = math.acos(N_vector[0] / N) if N_vector[1] >= 0.0 else 2 * math.pi - math.acos(N_vector[0] / N)
print("Ω = {} rad = {} deg".format(OMEGA, 360*OMEGA / (2*math.pi)))

omega = math.acos(np.dot(N_vector, e_vector) / (N * e)) if e_vector[2] >= 0.0 else 2 * math.pi - math.acos(np.dot(N_vector, e_vector) / (N * e))
print("ω = {} rad = {} deg".format(omega, 360*omega / (2*math.pi)))

theta = math.acos(np.dot(e_vector, r_vector) / (e*r)) if v_r >= 0.0 else 2*math.pi - math.acos(np.dot(e_vector, r_vector) / (e*r))
print("θ = {} rad = {} deg".format(theta, 360*theta / (2*math.pi)))
print(v_r)


# b)
perigee = (h * h) / (mi * (1 + e))
print('perigee: {}'.format(perigee))
z_min = perigee - earth_radius
print('z_min: {}'.format(z_min))
apogee = (h*h) / (mi * (1 - e))
print('apogee: {}'.format(apogee))
z_max = apogee
print('z_max: {}'.format(z_max))
print()

# c)


a = 0.5 * (perigee + apogee)
print("a = {} km".format(a))

T = 2*math.pi * math.pow(a, 1.5) / math.sqrt(mi)
print("T = {} s".format(T))

E_0 = math.atan( math.tan(theta/2) * math.sqrt((1-e)/(1+e)) ) * 2
print(theta, e)
print("E_0 = {} rad".format(E_0))

M_0 = E_0 - e * math.sin(E_0)
print("M_0 = {} rad".format(M_0))

t_0 = M_0 * T / (2 * math.pi)
print("t_0 = {}".format(t_0))

t_f = t_0 + delta_t
print("t_f = {}".format(t_f))

M_after = 2 * math.pi * t_f / T
print("M_after = {} rad".format(M_after))
# 2.5447546588387495 rad
# M_0 = 2.2390943250274646 rad
# t_0 = 15368.99736363939
# t_f = 27008.99736363939

def f(x):
    return x - e * math.sin(x) - M_after


E_after = fsolve(f, 1)
print("E_after = {} rad".format(E_after))

theta_after = 2 * np.arctan(np.sqrt((1 + e) / (1 - e)) * np.tan(E_after / 2))
print("theta_after = {} rad = {} deg".format(theta_after, math.degrees(theta_after)))

# a = 26580.380648270628 km
# T = 43127.37401990259 s
# 3.4729335610267182 0.5438506249284903
# E_0 = -2.54475465883875 rad
# M_0 = -2.2390943250274655 rad
# t_0 = -15368.997363639397
# t_f = -3728.997363639397
# M_after = -0.5432740104908291 rad
# E_after = [-1.00128605] rad
# omega_after = -1.5773488641105642 rad = -90.37543273328974 deg

