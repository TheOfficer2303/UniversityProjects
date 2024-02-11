from operator import matmul
import numpy as np

vector_a = np.array([[1], [3], [5]])
vector_b = np.array([[2], [4], [6]])

mat_mul = np.outer(vector_a, vector_b)
vect_dot = vector_a.transpose() @ vector_b
mat_exp = np.square(mat_mul)
sub_mat = mat_exp[1:3, 1:3]

print(mat_exp)
print(sub_mat)
