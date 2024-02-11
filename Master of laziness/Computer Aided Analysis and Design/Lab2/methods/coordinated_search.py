import copy
import math
from Lab2.methods.golden_ratio import golden_ratio
from functions.function import Function, Point

def minimise_lambda(value, f: Function = None, x: Point = None, i: int = None):
  x = copy.copy(x)
  x[i] += value

  return f.evaluate(x)


def coordinate_search(f: Function, x0: Point, e=10**-6):
  n = len(x0)
  x = copy.copy(x0)

  while True:
    xs = copy.copy(x)
    for i in range(n):
      function = Function("", lambda value: minimise_lambda(value, f=f, x=x, i = i))
      lambda_param = golden_ratio(function, x0=x[i])
      x[i] += lambda_param

    for i in range(n):
      if math.fabs(x[i] - xs[i]) > e:
        break
    else:
      break
    continue

  return x
