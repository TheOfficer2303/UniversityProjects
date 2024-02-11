from Lab1.matrix import Matrix
from functions.function import Point

def f3(x: Point):
  x1 = x[0]
  x2 = x[1]

  return (x1 - 2)**2 + (x2 + 3)**2
from Lab1.matrix import Matrix
from functions.function import Point

def f3_gradient(x: Point) -> Matrix:
  x1 = x[0]
  x2 = x[1]

  dx1 = 2 * (x1 - 2)
  dx2 = 2 * (x2 + 3)

  return Matrix(elements= [[dx1], [dx2]])

def f3_hessian(x: Point) -> Matrix:
  dx1dx1 = 2
  dx2dx1 = 0
  dx1dx2 = 0
  dx2dx2 = 2

  return Matrix(elements = [
    [dx1dx1, dx1dx2],
    [dx2dx1, dx2dx2]
  ])
