from typing import List
from domain.domainElement import DomainElement

from fuzzySet.fuzzy import CalculatedFuzzySet
from fuzzySet.operations.standard_functions import gamma_function, l_function, lambda_function
from rule import InputType, Rule
from system.defuzzifier.defuzzifier import IDefuzzifier
from system.domains import Domains
from system.fuzzy_system.fuzzy_system import FuzzySystem, FuzzySystemType
from system.fuzzy_system.input_sets import DistanceSets, SpeedSets

class AccelerationSets:
  BIG_ACCELERATE = CalculatedFuzzySet(Domains.ACCELERATION, gamma_function(
    Domains.ACCELERATION.index_of_element(DomainElement.of(20)),
    Domains.ACCELERATION.index_of_element(DomainElement.of(50)),
  ))

  ACCELERATE = CalculatedFuzzySet(Domains.ACCELERATION, gamma_function(
    Domains.ACCELERATION.index_of_element(DomainElement.of(45)),
    Domains.ACCELERATION.index_of_element(DomainElement.of(50)),
  ))

  DECCELERATE = CalculatedFuzzySet(Domains.ACCELERATION, l_function(
    Domains.ACCELERATION.index_of_element(DomainElement.of(-30)),
    Domains.ACCELERATION.index_of_element(DomainElement.of(-10)),
  ))

BIG_ACCELERATE_IF_VERY_FAR_FROM_LAND = Rule({
  InputType.L: DistanceSets.VERY_FAR_FROM_LAND,
  InputType.D: DistanceSets.VERY_FAR_FROM_LAND,
  InputType.LK: None,
  InputType.DK: None,
  InputType.V: None,
  InputType.S: None
  },
  AccelerationSets.BIG_ACCELERATE
)

ACCELERATE_IF_FAR_FROM_LAND = Rule({
  InputType.L: DistanceSets.FAR_FROM_LAND,
  InputType.D: DistanceSets.FAR_FROM_LAND,
  InputType.LK: DistanceSets.FAR_FROM_LAND,
  InputType.DK: DistanceSets.FAR_FROM_LAND,
  InputType.V: None,
  InputType.S: None
  },
  AccelerationSets.BIG_ACCELERATE
)

ACCELERATE_IF_GOING_SLOW = Rule({
  InputType.L: None,
  InputType.D: None,
  InputType.LK: None,
  InputType.DK: None,
  InputType.V: SpeedSets.SLOW,
  InputType.S: None
  },
  AccelerationSets.ACCELERATE
)

DECCELERATE_IF_GOING_FAST = Rule({
  InputType.L: None,
  InputType.D: None,
  InputType.LK: None,
  InputType.DK: None,
  InputType.V: SpeedSets.FAST,
  InputType.S: None
  },
  AccelerationSets.DECCELERATE
)

DECCELERATE_IF_CLOSE_TO_LAND = Rule({
  InputType.L: None,
  InputType.D: None,
  InputType.LK: DistanceSets.VERY_CLOSE_TO_LAND,
  InputType.DK: DistanceSets.VERY_CLOSE_TO_LAND,
  InputType.V: None,
  InputType.S: None
  },
  AccelerationSets.DECCELERATE
)

ACC_RULES_BASE = {
  'BIG_ACCELERATE_IF_VERY_FAR_FROM_LAND': BIG_ACCELERATE_IF_VERY_FAR_FROM_LAND,
  'ACCELERATE_IF_FAR_FROM_LAND': ACCELERATE_IF_FAR_FROM_LAND,
  'DECCELERATE_IF_GOING_FAST': DECCELERATE_IF_GOING_FAST,
  'DECCELERATE_IF_CLOSE_TO_LAND': DECCELERATE_IF_CLOSE_TO_LAND,
  # 'ACCELERATE_IF_GOING_SLOW': ACCELERATE_IF_GOING_SLOW
}


class AccelerationFuzzySystem(FuzzySystem):
  def __init__(self, defuzzifier: IDefuzzifier, rules = ACC_RULES_BASE) -> None:
    super().__init__(defuzzifier, rules, FuzzySystemType.MINIMUM)
