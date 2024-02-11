from typing import Tuple

from Lab1.matrix import Matrix

Point = Tuple[float, ...]
Vector = Tuple[float, ...]

class Function:
  def __init__(self, name, function, gradient = None, hessian: Matrix = None, jacobian: Matrix = None, G: Matrix = None, ) -> None:
    self.name = name
    self.function = function
    self._gradient = gradient
    self._hessian = hessian
    self._jacobian = jacobian
    self._G = G

    self.cache = {}
    self.gradient_cache = {}
    self.hessian_cache = {}

    self.count = 0
    self.gradient_count = 0
    self.hessian_count = 0

  def evaluate(self, value: float | Point):
    if not (isinstance(value, float) or isinstance(value, int)):
      value = tuple(value)

    if value in self.cache.keys():
      return self.cache[value]

    self.count += 1
    result = self.function(value)
    self.cache[value] = result

    return result

  def reset(self):
    self.cache = {}
    self.gradient_cache = {}
    self.hessian_cache = {}

    self.count = 0
    self.gradient_count = 0
    self.hessian_count = 0

  def gradient(self, point: Point) -> Matrix:
    if not (isinstance(point, float) or isinstance(point, int)):
      point = tuple(point)

    if point in self.gradient_cache.keys():
      return self.gradient_cache[point]

    result = self._gradient(point)
    self.gradient_cache[point] = result
    self.gradient_count += 1

    return result


  def hessian(self, point: Point) -> Matrix:
    if not (isinstance(point, float) or isinstance(point, int)):
      point = tuple(point)

    if point in self.hessian_cache.keys():
      return self.hessian_cache[point]

    result = self._hessian(point)
    self.hessian_cache[point] = result
    self.hessian_count += 1

    return result

  def jacobian(self, point: Point) -> Matrix:
    return self._jacobian(point)

  def G(self, point: Point) -> Matrix:
    return self._G(point)
