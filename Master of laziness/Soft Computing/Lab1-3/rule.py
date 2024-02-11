from __future__ import annotations
from enum import StrEnum, auto
from typing import List
from domain.domainElement import DomainElement
from fuzzySet.fuzzy import IFuzzySet
from fuzzySet.operations.operation_types import Operations


import dataclasses
from typing import List, Iterator


@dataclasses.dataclass
class InputValues:
    L: int
    D: int
    LK: int
    DK: int
    V: int
    S: int

    _current: int = dataclasses.field(init=False, default=0)
    _values: List[int] = dataclasses.field(init=False, default_factory=list)

    def __post_init__(self: InputValues) -> None:
        self._values = [self.L, self.D, self.LK, self.DK, self.V, self.S]

    def __iter__(self: InputValues) -> Iterator[int]:
        return iter(self._values)

class InputType(StrEnum):
  L = auto()
  D = auto()
  LK = auto()
  DK = auto()
  V = auto()
  S = auto()

class Rule:
  def __init__(self, antecedent: dict[InputType, IFuzzySet], consequent: IFuzzySet) -> None:
    self.antecedent = antecedent
    self.consequent = consequent

  def get_conclusion(self, values: InputValues, t_norm) -> IFuzzySet:
    alpha = 1

    for input_value, fuzzy_set in zip(values, self.antecedent.values()):

      if fuzzy_set is None:
        continue

      alpha = t_norm(alpha, fuzzy_set.get_value_at(DomainElement.of(input_value)))

    return Operations.unary_operation(self.consequent, lambda x: t_norm(x, alpha))
