import abc

from fuzzySet.fuzzy import IFuzzySet

class IDefuzzifier(abc.ABC):
  @abc.abstractmethod
  def defuzzify(self, fuzzy_set: IFuzzySet) -> float:
    pass

class COADefuzzifier(IDefuzzifier):
  def defuzzify(self, fuzzy_set: IFuzzySet) -> float:
    numerator = 0
    denominator = 0

    for element in fuzzy_set.get_domain():
      numerator += fuzzy_set.get_value_at(element) * element.get_component_value(0)
      denominator += fuzzy_set.get_value_at(element)

    return (numerator / denominator) if denominator != 0 else 1
