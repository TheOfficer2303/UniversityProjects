from typing import List, Tuple

Point = Tuple[float, ...]

class Function:
  def __init__(self, name, function) -> None:
    self.name = name
    self.function = function
    self.cache = {}
    self.count = 0

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
    self.count = 0
    self.cache = {}
