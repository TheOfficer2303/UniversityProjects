from copy import copy

from Lab3.functions.function import Function, Point


def hooke_jeeves(f: Function, x0: Point, dx = 0.5, e = 10**-6):
  n = len(x0)
  xp = copy(x0)
  xb = copy(x0)

  while True:
    xn = search(f, xp, dx)

    if f.evaluate(xn) < f.evaluate(xb):
      # xP = 2xN - xB;
      for i in range(n):
        xp[i] = 2 * xn[i] - xb[i]
      xb = copy(xn)
    else:
      dx *= 0.5
      xp = copy(xb)

    if dx <= 0.5 * e:
      return xb

def search(f:Function, xp: Point, dx: float):
  x = copy(xp)
  n = len(x)

  for i in range(n):
    P = f.evaluate(x)

    # xi = xi + Dx
    x[i] += dx

    N = f.evaluate(x)

    if N > P:
      # xi = xi - 2Dx
      x[i] -= 2 * dx

      N = f.evaluate(x)
      if N > P:
        # xi = xi + Dx
        x[i] += dx

  return x
