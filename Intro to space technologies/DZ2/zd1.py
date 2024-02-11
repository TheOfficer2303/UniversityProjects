import numpy as np

# Initial data
b_i = np.array([22.2, 1.7, 42.7])
n = np.array([-1, 1, -4])
alpha = np.radians(65)

# 1
n_magnitude = np.linalg.norm(n)
print('|n| = {}'.format(n_magnitude))
print()

# 2
n_normalized = n / n_magnitude
print('n = {}i + {}j + {}k'.format(n_normalized[0], n_normalized[1], n_normalized[2]))
print()

# 3
q1 = np.cos(alpha / 2)
q2 = n_normalized[0] * np.sin(alpha / 2)
q3 = n_normalized[1] * np.sin(alpha / 2)
q4 = n_normalized[2] * np.sin(alpha / 2)

q = np.array([q1, q2, q3, q4])
q_magnitude = np.linalg.norm(q)
q_normalized = q / q_magnitude
print('q = {} + {}i + {}j + {}k'
      .format(q_normalized[0], q_normalized[1], q_normalized[2], q_normalized[3]))
print()


# 4
print('|q| = {}'.format(q_magnitude))
print()

# 5
r11 = q1 * q1 + q2 * q2 - q3 * q3 - q4 * q4
r12 = 2 * (q2 * q3 + q1 * q4)
r13 = 2 * (q2 * q4 - q1 * q3)
r21 = 2 * (q2 * q3 - q1 * q4)

r22 = q1 * q1 - q2 * q2 + q3 * q3 - q4 * q4
r23 = 2 * (q3 * q4 + q1 * q2)
r31 = 2 * (q2 * q4 + q1 * q3)
r32 = 2 * (q3 * q4 - q1 * q2)

r33 = q1 * q1 - q2 * q2 - q3 * q3 + q4 * q4

psi = np.arctan2(r12, r11)
theta = np.arcsin(-r13)
phi = np.arctan2(r23, r33)

print('Ψ = {}°'.format(np.degrees(psi)))
print('θ = {}°'.format(np.degrees(theta)))
print('ϕ = {}°'.format(np.degrees(phi)))
print()

# 6
print('r_11 = {}'.format(r11))
print('r_12 = {}'.format(r12))
print('r_13 = {}'.format(r13))
print('r_21 = {}'.format(r21))
print('r_22 = {}'.format(r22))
print('r_23 = {}'.format(r23))
print('r_31 = {}'.format(r31))
print('r_32 = {}'.format(r32))
print('r_33 = {}'.format(r33))
print()

# 7
R = np.array([
    [r11, r12, r13],
    [r21, r22, r23],
    [r31, r32, r33]
])
b_b = np.dot(R, b_i)
print('b_b = {}i + {}j + {}k'.format(b_b[0], b_b[1], b_b[2]))
print()

# 8
b_i_magnitude = np.linalg.norm(b_i)
b_b_magnitude = np.linalg.norm(b_b)
print('|b_i| = {}'.format(b_i_magnitude))
print('|b_b| = {}'.format(b_b_magnitude))
print()
