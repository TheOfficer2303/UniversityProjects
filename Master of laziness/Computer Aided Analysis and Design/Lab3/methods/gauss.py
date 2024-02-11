from copy import copy
from functions.function import Function, Point
from methods.gradient import euclid_norm


def gauss_newton(x0: Point, f: Function = None, jacobian_0 = None, G_0 = None, use_golden_ratio=True, e=10**-6):
  x = copy(x0)
  if f:
    f_old = f.evaluate(x)
    count = 0

  while True:
    if f and count == 10:
      return f"Divergencija, zapao u točki {x}, vrijednost f(x): {f_old}"
    if f:
      J = f.jacobian(x)
      G = f.G(x)
    else:
      J = jacobian_0(x)
      G = G_0(x)

    A = ~J * J
    g = ~J * G

    delta_x = A.lup_solve(-g)
    if delta_x == "Fail":
      return x

    for i in range(len(x)):
      x[i] += delta_x[i]

    if euclid_norm(delta_x) < e:
      return x

    if f:
      f_new = f.evaluate(x)
      if round(f_old, 10) <= round(f_new, 10):
        count += 1
      else:
        count = 0
      f_old = f_new
