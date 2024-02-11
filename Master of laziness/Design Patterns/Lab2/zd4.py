from abc import ABC, abstractmethod
from dataclasses import dataclass
from math import ceil
from random import gauss

import numpy

class INumberGenerator(ABC):
  @abstractmethod
  def method_name(self):
    return "Generator"

  @abstractmethod
  def generate(self):
    pass


class IPercentilCalculation(ABC):
  @abstractmethod
  def method_name(self):
    pass

  @abstractmethod
  def calculate(self, numbers, percentile):
    pass


@dataclass
class LinearNumberGenerator(INumberGenerator):
  start: int
  stop: int
  step: int

  def method_name(self):
    return "Linear number generator"

  def generate(self):
    numbers = []

    for i in range(self.start, self.stop, self.step):
       numbers.append(i)

    return numbers


@dataclass
class NormalDistributionNumberGenerator(INumberGenerator):
  n: int
  sigma: float
  mean: float

  def method_name(self):
    return "Normal distribution generator"

  def generate(self):
    numbers = []

    for _ in range(self.n):
       numbers.append(round(gauss(self.mean, self.sigma), 2))

    return numbers


@dataclass
class FibonacciNumberGenerator(INumberGenerator):
  n: int

  def method_name(self):
    return "Fibonnaci generator"

  def generate(self):
    numbers = []

    i_curr = 0
    i_next = 1
    for _ in range(self.n):
      i_n = i_curr + i_next
      numbers.append(i_n)

      i_curr = i_next
      i_next = i_n

    return numbers


@dataclass
class NearestRankPercentile(IPercentilCalculation):
  def method_name(self):
    return "Nearest rank"

  def calculate(self, numbers, percentile):
    sorted_numbers = sorted(numbers)
    N = len(numbers)
    n = ceil(percentile / 100 * N)

    return sorted_numbers[n - 1]


@dataclass
class LinearInterpolationPercentile(IPercentilCalculation):
  def method_name(self):
    return "Linear Interpolation"

  def calculate(self, numbers, percentile):
    sorted_numbers = sorted(numbers)
    return round(numpy.percentile(sorted_numbers, percentile), 2)


@dataclass
class DistributionTester:
  numberGenerator: INumberGenerator
  percentileCalculator: IPercentilCalculation

  def get_numbers(self):
     return self.numberGenerator.generate()

  def get_percentile(self, numbers, percentile):
    return self.percentileCalculator.calculate(numbers, percentile)


def main():
  generators: list[INumberGenerator] = [LinearNumberGenerator(1, 20, 2), FibonacciNumberGenerator(20), NormalDistributionNumberGenerator(10, 25, 5)]
  percentileMethods = [NearestRankPercentile(), LinearInterpolationPercentile()]
  percentiles = [i for i in range(10, 100, 10)]

  for generator in generators:
    for pm in percentileMethods:
      dt = DistributionTester(generator, pm)

      numbers = dt.get_numbers()
      print(f"Numbers generated with {generator.method_name()}: {numbers}")

      for p in percentiles:
        percentile = dt.get_percentile(numbers, p)
        print(f"{p}th percentile calculated with {pm.method_name()}: {percentile}")


if __name__ == "__main__":
  main()
