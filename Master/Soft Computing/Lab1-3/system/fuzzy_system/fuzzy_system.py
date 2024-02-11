from enum import StrEnum, auto
from typing import List
from fuzzySet.fuzzy import IFuzzySet
from fuzzySet.operations.binary_operations import zadeh_and, zadeh_or
from fuzzySet.operations.operation_types import Operations
from rule import InputValues, Rule
from system.defuzzifier.defuzzifier import IDefuzzifier

class FuzzySystemType(StrEnum):
    MINIMUM = auto()
    MAXIMUM = auto()

class FuzzySystem:
  def __init__(self, defuzzifier: IDefuzzifier, rules: dict[str, Rule], type) -> None:
    self.defuzzifier = defuzzifier
    self.rules = rules
    self.type = type

    if self.type == FuzzySystemType.MINIMUM:
      self.t_norm = zadeh_and()
    else:
      raise ValueError

    self.s_norm = zadeh_or()

  def decide(self, values: InputValues):
    consequents: List[IFuzzySet] = []

    for rule in self.rules.values():
      consequents.append(rule.get_conclusion(values, zadeh_and()))

    result = consequents[0]
    for consequent in consequents:
      result = Operations.binary_operation(result, consequent, zadeh_or())

    defuzzified_result = round(self.defuzzifier.defuzzify(result))

    return defuzzified_result
