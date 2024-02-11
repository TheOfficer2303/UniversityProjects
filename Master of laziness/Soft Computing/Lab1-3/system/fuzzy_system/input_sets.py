from domain.domainElement import DomainElement
from fuzzySet.fuzzy import CalculatedFuzzySet, MutableFuzzySet
from fuzzySet.operations.standard_functions import gamma_function, l_function
from system.domains import Domains

class OrientantionSets:
  WRONG_DIRECTION = MutableFuzzySet(Domains.ORIENTATION).set_value(DomainElement.of(0), 1)

class DistanceSets:
  CLOSE_TO_LAND = CalculatedFuzzySet(Domains.DISTANCE, l_function(40, 70))

  VERY_CLOSE_TO_LAND = CalculatedFuzzySet(Domains.DISTANCE, l_function(30, 40))

  VERY_FAR_FROM_LAND = CalculatedFuzzySet(Domains.DISTANCE, l_function(120, 220))

  FAR_FROM_LAND = CalculatedFuzzySet(Domains.DISTANCE, l_function(100, 200))

class SpeedSets:
  FAST = CalculatedFuzzySet(Domains.SPEED, gamma_function(
    Domains.SPEED.index_of_element(DomainElement.of(50)),
    Domains.SPEED.index_of_element(DomainElement.of(60)),
  ))

  SLOW = CalculatedFuzzySet(Domains.SPEED, gamma_function(
      Domains.SPEED.index_of_element(DomainElement.of(30)),
      Domains.SPEED.index_of_element(DomainElement.of(40)),
  ))
