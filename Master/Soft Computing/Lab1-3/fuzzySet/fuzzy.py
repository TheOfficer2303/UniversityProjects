from __future__ import annotations

from abc import ABC, abstractmethod
import copy
from typing import List

from domain.domain import IDomain
from domain.domainElement import DomainElement


class IFuzzySet(ABC):
  @abstractmethod
  def get_domain() -> IDomain:
    pass
  @abstractmethod
  def get_value_at(d: DomainElement) -> float:
    pass

class MutableFuzzySet(IFuzzySet):
  def __init__(self, domain: IDomain) -> None:
    self.memberships = [0.0] * domain.get_cardinality()
    self.domain = copy.deepcopy(domain)

  def get_domain(self) -> IDomain:
    return self.domain

  def get_value_at(self, d: DomainElement) -> float:
    return self.memberships[self.domain.index_of_element(d)]

  def set_value(self, d: DomainElement, value: float) -> MutableFuzzySet:
    self.memberships[self.domain.index_of_element(d)] = value

    return self


class CalculatedFuzzySet(IFuzzySet):
  def __init__(self, domain: IDomain, int_unary_function) -> None:
    self.domain = domain
    self.int_unary_function = int_unary_function

  def get_domain(self) -> IDomain:
    return self.domain

  def get_value_at(self, d: DomainElement) -> float:
    return self.int_unary_function(self.domain.index_of_element(d))
