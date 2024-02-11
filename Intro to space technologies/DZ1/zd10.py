from math import floor
from math import pow

y = 2022
m = 6
d = 17

cet = 23.5
ut = cet - 1

e = 15.971389

j0 = 367.0 * y - floor((7.0 * (y + floor((m+9.0)/12.0)))/4.0) + floor(275.0*m/9.0) + d + 1721013.5
print("J0 = {}".format(j0))

jd = j0 + ut/24.0
print("JD = {}".format(jd))

t0 = (j0 - 2451545.0)/36525.0
print("T0 = {}".format(t0))

theta_g_0h_ut = 100.4606184 + 36000.77004 * t0 + 0.000387933 * t0 * t0 - 2.583 * pow(10, -8) * pow(t0, 3)
theta_g_0h_ut -= 360.0 * floor(theta_g_0h_ut / 360.0)
print("theta_g_0h_ut = {}".format(theta_g_0h_ut))

theta_g_cet_ut = theta_g_0h_ut + 0.00417807 * (ut/24) * 24 * 3600
theta_g_cet_ut -= 360.0 * floor(theta_g_cet_ut / 360.0)
print("theta_g_cet_ut = {}".format(theta_g_cet_ut))

theta_zg = theta_g_cet_ut + e
print("theta_zg = {}".format(theta_zg))
