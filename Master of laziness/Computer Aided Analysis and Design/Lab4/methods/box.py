from copy import copy
from math import sqrt
from random import random
from typing import List

import numpy as np
from Lab2.methods.simplex import find_centroid, reflexion
from Lab3.functions.function import Function, Point

# g - implicitna ogranicenja
def box(f: Function, x0: Point, xd = -10, xg = 10, g = (), alpha=1.3, e=10e-6):
  xc = copy(x0)
  X: List[Point] = [copy(x0)]

  n = len(x0)

  for i in range(2 * n):
    new_point: Point = list((xd + np.random.rand(n, ) * (xg - xd)))

    while any(gi(new_point) < 0 for gi in g):
      for i in range(len(new_point)):
        new_point[i] = 0.5 * (new_point[i] + xc[i])

    X.append(tuple(new_point))
    xc = find_centroid(X)

  while True:
    func_values = []
    for i in range(len(X)):
      func_values.append(f.evaluate(X[i]))

    h2, h = np.argsort(func_values)[-2:]

    xc = find_centroid(X, h)
    xr = reflexion(xc, X[h], alpha)

    for i in range(n):
      if xr[i] < xd:
        xr[i] = xd
      elif xr[i] > xg :
        xr[i] = xg

    while any(gi(xr) < 0 for gi in g):
      for i in range(len(new_point)):
        xr[i] = 0.5 * (xr[i] + xc[i])

    if f.evaluate(xr) > f.evaluate(X[h2]):
      for i in range(len(new_point)):
        xr[i] = 0.5 * (xr[i] + xc[i])

    X[h] = xr

    value = 0
    for point in X:
      value += (f.evaluate(point) - f.evaluate(xc)) ** 2

    value *= 1 / 2
    value = sqrt(value)

    if value < e:
      return xc
