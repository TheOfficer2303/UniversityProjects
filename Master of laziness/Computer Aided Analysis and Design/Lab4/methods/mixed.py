from copy import copy
from math import sqrt
import math
from random import random
from typing import List

import numpy as np
from Lab2.methods.hooke_jeeves import hooke_jeeves
from Lab2.methods.simplex import find_centroid, reflexion
from Lab3.functions.function import Function, Point

def mixed(f: Function, x0: Point, t0=10, g = (), h = (), e=10e-6):
  x = copy(x0)
  t = copy(t0)

  if any(gi(x) < 0 for gi in g):
    x = hooke_jeeves(Function("", find_inner(g)), x)

  while True:
    xs = copy(x)
    x = hooke_jeeves(Function("Optimizacija s ogranicenjem", F(f, g, h, t)), x)

    t *= 10

    if all(math.isclose(a, b, abs_tol=e) for a, b in zip(xs, x)):
      return x

def F(f: Function, g, h, t):
  def _F(x: Point):
    result = f.evaluate(x)

    for constraint in g:
      if constraint(x) <= 0:
        return math.inf

      result += (1 / t) * math.log(constraint(x))


    for constraint in h:
      result += t * constraint(x) ** 2

    return result

  return _F

def find_inner(g):
  def _find(x: Point):
    result = 0
    for gi in g:
      if gi(x) < 0:
        result -= gi(x)

    return result

  return _find
