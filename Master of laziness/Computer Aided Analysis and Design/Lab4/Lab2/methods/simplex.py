from math import sqrt
from typing import List
import numpy as np
from copy import copy

from Lab3.functions.function import Point, Function

def find_centroid(X: List[Point], h: Point=None) -> Point:
  total_points = len(X)

  if h:
    filtered_points = [X[i] for i in range(total_points) if i != h]
    total_points -= 1
  else:
    filtered_points = X

  centroid = [sum(coord) / (total_points) for coord in zip(*filtered_points)]

  return centroid

def reflexion(xc: Point, xh: Point, alpha) -> Point:
  xr = copy(xc)
  for i in range(len(xc)):
    xr[i] = (1 + alpha) * xc[i] - alpha * xh[i]

  return xr

def expansion(xc: Point, xr: Point, gamma):
  xe = copy(xr)
  for i in range(len(xc)):
    xe[i] = (1 - gamma) * xc[i] - gamma * xr[i]

  return xe

def contraction(xc: Point, x: Point, alpha, beta):
  xk = copy(xc)
  for i in range(len(xc)):
    xk[i] = (1 - beta) * xc[i] - alpha * x[i]

  return xk


def nelder_mead_simplex(f: Function, x0: Point, step = 1.0, alpha = 1, beta = 0.5, gamma = 2, sigma = 0.5, e=10e-6):
  X = [copy(x0)]

  for i in range(len(x0)):
    new = copy(x0)
    new[i] += step
    X.append(new)

  while True:
    func_values = []
    for i in range(len(X)):
      func_values.append(f.evaluate(X[i]))

    h = np.argmax(func_values)
    l = np.argmin(func_values)

    xc = find_centroid(X, h)

    xr = reflexion(xc, X[h], alpha)

    if f.evaluate(xr) < f.evaluate(X[l]):
      xe = expansion(xc, xr, gamma)

      X[h] = xe if f.evaluate(xe) < f.evaluate(X[l]) else xr
    else:
      if all(f.evaluate(xr) > f.evaluate(X[i]) for i in range(len(X)) if i != h):
        if f.evaluate(xr) < f.evaluate(X[h]):
          X[h] = xr

        xk = contraction(xc, X[h], alpha, beta)

        if f.evaluate(xk) < f.evaluate(X[h]):
          X[h] = xk
        else:
          for i, point in enumerate(X):
            if i == l:
              continue

            for j in range(len(point)):
              point[j] = sigma * (X[i][j] + X[l][j])
      else:
        X[h] = xr

    value = 0
    for point in X:
        value += (f.evaluate(point) - f.evaluate(xc)) ** 2

    value *= 1 / 2
    value = sqrt(value)

    if value < e:
      return xc
