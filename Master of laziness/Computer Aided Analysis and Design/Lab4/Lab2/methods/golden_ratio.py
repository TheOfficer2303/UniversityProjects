import math
from functions.function import Function


def golden_ratio(f: Function, a: float = None, b: float = None, x0: float = None, e = 10**-6) -> int:
  if x0 is not None:
    a, b = find_unimodal_interval(f, x0)

  k = (math.sqrt(5) - 1) * 0.5
  c = b - k * (b - a)
  d = a + k * (b - a)
  fc = f.evaluate(c)
  fd = f.evaluate(d)

  while b - a > e:
    if fc < fd:
      b = d
      d = c
      c = b - k * (b - a)
      fd = fc
      fc = f.evaluate(c)
    else:
      a = c
      c = d
      d = a + k * (b - a)
      fc = fd
      fd = f.evaluate(d)

  return (a + b) / 2


def find_unimodal_interval(f: Function, point: float, h=1):
  l = point - h
  r = point + h
  m = point
  step = 1

  fm = f.evaluate(point);
  fl = f.evaluate(l);
  fr = f.evaluate(r);

  if fm < fr and fm < fl:
    return l, r
  elif fm > fr:
    while fm > fr:
      l = m
      m = r
      fm = fr
      step *= 2
      r = point + h * step
      fr = f.evaluate(r)
  else:
    while fm > fl:
      r = m
      m = l
      fm = fl
      step *= 2
      l = point - h * step
      fl = f.evaluate(l)

  return l, r
