import numpy as np

# Initial data
a = 0.1
conductor_length = 149
N = conductor_length / (4 * a)
current = 114 * (10 ** -3)
r = 0.18 * (10 ** -3)

# 2
m_magnitude = np.sqrt(2) * N * current * (a ** 2)
print('|m| = {} Am^2'.format(m_magnitude))
print()

# 3
B = 34 * (10 ** -6)
tau_magnitude = N * current * (a ** 2) * B  # * np.sin(90 degrees) == 1
print('|tau| = {} Nm'.format(tau_magnitude))
print()

# 4
S = (r ** 2) * np.pi
resistance = 1.68 * (10 ** -8)
R = resistance * conductor_length / S
print('R = {} Ohm'.format(R))
print()

# 5
P = (current ** 2) * R
print('P = {} W'.format(P))
print()

# 6
satellite_mass = 1
satellite_size = 0.1
satellite_I = satellite_mass * (satellite_size ** 2) / 6
print('I = {} kgm^2'.format(satellite_I))
print()

# 7
omega = np.radians(25)
M = (10 ** -5)
alpha = M / satellite_I
t = omega / alpha
print('t = {} s'.format(t))
print()