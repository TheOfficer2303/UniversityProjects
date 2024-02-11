from Lab1.matrix import Matrix
from functions.function import Point

def f4(x: Point):
  x1 = float(x[0])
  x2 = float(x[1])

  return 0.25 * x1 ** 4 - x1 ** 2 + 2 * x1 + (x2 - 1) ** 2

def f4_gradient(x: Point):
  x1 = x[0]
  x2 = x[1]

  dx1 = x1 ** 3 - 2 * x1 + 2
  dx2 = 2 * x2 - 4

  return Matrix(elements=[[dx1], [dx2]])

def f4_hessian(x: Point):
  x1 = x[0]
  x2 = x[1]

  dx1dx1 = 3 * x1 ** 2 - 2
  dx1dx2 = 0
  dx2dx1 = 0
  dx2dx2 = 2

  return Matrix(elements = [
    [dx1dx1, dx1dx2],
    [dx2dx1, dx2dx2]
  ])
