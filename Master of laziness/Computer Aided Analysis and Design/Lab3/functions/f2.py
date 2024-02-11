from Lab1.matrix import Matrix
from functions.function import Point

def f2(x: Point):
  if len(x) != 2:
    raise ValueError("Function is 2d")

  x1 = x[0]
  x2 = x[1]

  return (x1 - 4)**2 + 4 * ((x2 - 2)**2)

def f2_gradient(x: Point):
  x1 = x[0]
  x2 = x[1]

  dx1 = 2 * (x1 - 4)
  dx2 = 8 * (x2 - 2)

  return Matrix(elements=[[dx1], [dx2]])

def f2_hessian(x: Point):
  dx1dx1 = 2
  dx2dx1 = 0
  dx1dx2 = 0
  dx2dx2 = 8

  return Matrix(elements = [
    [dx1dx1, dx1dx2],
    [dx2dx1, dx2dx2]
  ])
