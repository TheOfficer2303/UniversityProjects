from copy import copy
from Lab1.matrix import Matrix
from functions.function import Function, Point, Vector
from Lab2.methods.golden_ratio import golden_ratio

def euclid_norm(vector: Matrix):
  sum = 0
  for i in range(vector.row_count):
    sum += vector[i] ** 2

  return sum ** 0.5
  return sum(x ** 2 for x in vector) ** 0.5


def minimise_lambda(value, f: Function = None, x: Point = None, gradient: Vector = None):
  x = copy(x)
  for i in range(len(x)):
    x[i] += value * gradient[i]
  return f.evaluate(x)


def gradient_descent(f: Function, x0: Point, newton_method = False, use_golden_ratio=True, e=10**-6):
  x = copy(x0)
  n = len(x)
  gradient_at_x = f.gradient(x)
  hessian_at_x = f.hessian(x)

  f_old = f.evaluate(x)
  count = 0

  while euclid_norm(gradient_at_x) >= e:
    if count == 100:
      return f"Divergencija, zapao u točki {x}, vrijednost f(x): {f_old}"

    if newton_method:
      delta_x = -hessian_at_x.inverse() * gradient_at_x
    else:
      delta_x = gradient_at_x

    if use_golden_ratio:
      function = Function("", lambda value: minimise_lambda(value, f=f, x=x, gradient=delta_x))
      optimal_lambda = golden_ratio(function, x0=0.0)
      for i in range(n):
        x[i] += optimal_lambda * delta_x[i]

    else:
      for i in range(len(x)):
        x[i] -= delta_x[i]

    gradient_at_x = f.gradient(x)
    hessian_at_x = f.hessian(x)

    f_new = f.evaluate(x)
    if round(f_old, 10) <= round(f_new, 10):
      count += 1
    else:
      count = 0
    f_old = f_new
    # print(x)

  return x
