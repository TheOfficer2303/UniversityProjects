from __future__ import annotations

from abc import ABC, abstractmethod
import copy
import itertools
from typing import Iterable, Iterator, List

from domain.domainElement import DomainElement

class IDomain(ABC, Iterable[DomainElement]):
  @abstractmethod
  def get_cardinality(self) -> int:
    pass
  def get_component(self, index: int) -> IDomain:
    pass
  def get_number_of_components(self) -> int:
    pass
  def index_of_element(self, element: DomainElement) -> int:
    pass
  def element_for_index(self, index: int) -> DomainElement:
    pass

class Domain(IDomain, ABC):
  @staticmethod
  def int_range(first: int, last: int) -> IDomain:
    if first > last:
      raise ValueError("First value must be smaller than the last value")

    return SimpleDomain(first, last)

  @staticmethod
  def combine(d1: IDomain, d2: IDomain) -> IDomain:
    domains = []
    d1 = copy.deepcopy(d1)
    d2 = copy.deepcopy(d2)

    for i in range(d1.get_number_of_components()):
      if isinstance(d1.get_component(i), SimpleDomain):
        domains.append(d1.get_component(i))

    for i in range(d2.get_number_of_components()):
      if isinstance(d2.get_component(i), SimpleDomain):
        domains.append(d2.get_component(i))

    return CompositeDomain(domains)

  def index_of_element(self, element: DomainElement) -> int:
    for index, el in enumerate(self):
      if el == element:
        return index

    raise ValueError(f"Element {element} not found")

  def element_for_index(self, index: int) -> DomainElement:
    for i, element in enumerate(self):
      if i == index:
        return element

    raise ValueError(f"Cannot find element with index {index}")

class SimpleDomain(Domain):
  def __init__(self, first: int, last: int):
    self._current_iter = None
    self.first = first
    self.last = last

  def get_cardinality(self) -> int:
    return self.last - self.first

  def get_component(self, index: int) -> IDomain:
    return self

  def get_number_of_components(self) -> int:
    return 1

  def index_of_element(self, element: DomainElement) -> int:
    return element.get_component_value(0) - self.first

  def element_for_index(self, index: int) -> DomainElement:
    return DomainElement.of(self.first + index)

  def __iter__(self) -> Iterator[DomainElement]:
    self._current_iter = self.first
    return self

  def __next__(self):
    if self._current_iter < self.last:
      next_value = DomainElement((self._current_iter, ))
      self._current_iter += 1
      return next_value
    else:
      raise StopIteration

class CompositeDomain(Domain):
  def __init__(self, domains: List[SimpleDomain]):
    self.domains = domains
    self.cartesian = None

  def get_cardinality(self) -> int:
    cardinality = 1

    for domain in self.domains:
      cardinality *= domain.get_cardinality()

    return cardinality

  def get_component(self, index: int) -> IDomain:
    return self.domains[index]

  def get_number_of_components(self) -> int:
    return len(self.domains)

  def __iter__(self) -> Iterator[DomainElement]:
    ranges = []

    for domain in self.domains:
      ranges.append(range(domain.first, domain.last))

    self.cartesian = itertools.product(*ranges)
    return self

  def __next__(self) -> DomainElement:
    return DomainElement(self.cartesian.__next__())
