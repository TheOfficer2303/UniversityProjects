from copy import deepcopy
from domain.domain import Domain
from fuzzySet.fuzzy import IFuzzySet, MutableFuzzySet


class Operations:
  @staticmethod
  def unary_operation(fuzzy_set: IFuzzySet, unary_function) -> IFuzzySet:
    new_set = MutableFuzzySet(deepcopy(fuzzy_set.get_domain()))

    for i in range(fuzzy_set.get_domain().get_cardinality()):
      old_element = fuzzy_set.get_domain().element_for_index(i)
      old_value = fuzzy_set.get_value_at(old_element)

      new_element = new_set.get_domain().element_for_index(i)
      new_value = unary_function(old_value)

      new_set = new_set.set_value(new_element, new_value)

    return new_set

  @staticmethod
  def binary_operation(set1: IFuzzySet, set2: IFuzzySet, binary_function) -> IFuzzySet:
    if set1.get_domain().get_cardinality() != set2.get_domain().get_cardinality():
      raise ValueError("Sets must be of the same cardinality")

    new_set = MutableFuzzySet(deepcopy(set1.get_domain()))

    for i in range(set1.get_domain().get_cardinality()):
      old_set1_element = set1.get_domain().element_for_index(i)
      old_set1_value = set1.get_value_at(old_set1_element)

      old_set2_element = set2.get_domain().element_for_index(i)
      old_set2_value = set2.get_value_at(old_set2_element)

      new_element = new_set.get_domain().element_for_index(i)
      new_value = binary_function(old_set1_value, old_set2_value)

      new_set = new_set.set_value(new_element, new_value)

    return new_set
