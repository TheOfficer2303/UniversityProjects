from Lab1.matrix import Matrix
from functions.function import Point

def f1(x: Point):
  if len(x) != 2:
    raise ValueError("Function is 2d")

  x1 = x[0]
  x2 = x[1]

  return 100 * (x2 - x1**2)**2 + (1 - x1)**2

def f1_gradient(x: Point) -> Matrix:
  x1 = x[0]
  x2 = x[1]

  dx1 = 400 * x1**3 - 400 * x1 * x2 + 2 * x1 - 2
  dx2 = -200 * x1**2 + 200 * x2

  return Matrix(elements=[[dx1], [dx2]])

def f1_hessian(x: Point) -> Matrix:
  x1 = x[0]
  x2 = x[1]

  dx1dx1 = 1200 * x1**2 - 400 * x2 + 2
  dx2dx1 = -400 * x1
  dx1dx2 = -400 * x1
  dx2dx2 = 200

  return Matrix(elements = [
    [dx1dx1, dx1dx2],
    [dx2dx1, dx2dx2]
  ])

def f1_jacobian(x: Point) -> Matrix:
  x1 = x[0]
  x2 = x[1]

  return Matrix(elements= [
    [400 * x1 * (x1 ** 2 - x2), -200 * x1**2 + 200 * x2],
    [2 * x1 - 2, 0]
  ])

def f1_G(x: Point) -> Matrix:
  x1 = x[0]
  x2 = x[1]

  return Matrix(elements=[
    [100 * (x2 - x1**2)**2],
    [(1 - x1)**2]
  ])
