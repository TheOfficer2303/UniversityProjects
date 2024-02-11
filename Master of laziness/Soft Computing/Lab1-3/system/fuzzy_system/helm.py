from typing import List
from domain.domainElement import DomainElement

from fuzzySet.fuzzy import CalculatedFuzzySet
from fuzzySet.operations.standard_functions import gamma_function, l_function, lambda_function
from rule import InputType, Rule
from system.defuzzifier.defuzzifier import IDefuzzifier
from system.domains import Domains
from system.fuzzy_system.fuzzy_system import FuzzySystem, FuzzySystemType
from system.fuzzy_system.input_sets import DistanceSets, OrientantionSets, SpeedSets

class AngleSets:
  LEFT_TURN_SOFT = CalculatedFuzzySet(Domains.ANGLE, gamma_function(
    Domains.ANGLE.index_of_element(DomainElement.of(5)),
    Domains.ANGLE.index_of_element(DomainElement.of(30)),
))

  RIGHT_TURN_SOFT = CalculatedFuzzySet(Domains.ANGLE, l_function(
      Domains.ANGLE.index_of_element(DomainElement.of(-30)),
      Domains.ANGLE.index_of_element(DomainElement.of(-5)),
  ))

  LEFT_TURN_HARD = CalculatedFuzzySet(Domains.ANGLE, gamma_function(
      Domains.ANGLE.index_of_element(DomainElement.of(30)),
      Domains.ANGLE.index_of_element(DomainElement.of(90)),
  ))

  RIGHT_TURN_HARD = CalculatedFuzzySet(Domains.ANGLE, l_function(
      Domains.ANGLE.index_of_element(DomainElement.of(-90)),
      Domains.ANGLE.index_of_element(DomainElement.of(-30)),
  ))

LEFT_TURN_HARD_IF_D_VERY_CLOSE = Rule({
  InputType.L: None,
  InputType.D: DistanceSets.VERY_CLOSE_TO_LAND,
  InputType.LK: None,
  InputType.DK: None,
  InputType.V: None,
  InputType.S: None
  },
  AngleSets.LEFT_TURN_HARD
)

LEFT_TURN_HARD_IF_DK_VERY_CLOSE = Rule({
  InputType.L: None,
  InputType.D: None,
  InputType.LK: None,
  InputType.DK: DistanceSets.VERY_CLOSE_TO_LAND,
  InputType.V: None,
  InputType.S: None
  },
  AngleSets.LEFT_TURN_HARD
)

RIGHT_TURN_HARD_IF_L_VERY_CLOSE = Rule({
  InputType.L: DistanceSets.VERY_CLOSE_TO_LAND,
  InputType.D: None,
  InputType.LK: None,
  InputType.DK: None,
  InputType.V: None,
  InputType.S: None
  },
  AngleSets.RIGHT_TURN_HARD
)

RIGHT_TURN_HARD_IF_LK_VERY_CLOSE = Rule({
  InputType.L: None,
  InputType.D: None,
  InputType.LK: DistanceSets.VERY_CLOSE_TO_LAND,
  InputType.DK: None,
  InputType.V: None,
  InputType.S: None
  },
  AngleSets.RIGHT_TURN_HARD
)

LEFT_TURN_SOFT_IF_D_CLOSE = Rule({
  InputType.L: None,
  InputType.D: DistanceSets.CLOSE_TO_LAND,
  InputType.LK: None,
  InputType.DK: DistanceSets.CLOSE_TO_LAND,
  InputType.V: None,
  InputType.S: None
  },
  AngleSets.LEFT_TURN_SOFT
)

RIGHT_TURN_SOFT_IF_L_CLOSE = Rule({
  InputType.L: DistanceSets.CLOSE_TO_LAND,
  InputType.D: None,
  InputType.LK: DistanceSets.CLOSE_TO_LAND,
  InputType.DK: None,
  InputType.V: None,
  InputType.S: None
  },
  AngleSets.RIGHT_TURN_SOFT
)

RIGHT_TURN_HARD_IF_WRONG_WAY = Rule({
  InputType.L: DistanceSets.FAR_FROM_LAND,
  InputType.D: DistanceSets.FAR_FROM_LAND,
  InputType.LK: None,
  InputType.DK: None,
  InputType.V: None,
  InputType.S: OrientantionSets.WRONG_DIRECTION
  },
  AngleSets.RIGHT_TURN_SOFT
)


HELM_RULES_BASE = {
  'LEFT_TURN_HARD_IF_D_VERY_CLOSE': LEFT_TURN_HARD_IF_D_VERY_CLOSE,
  'LEFT_TURN_HARD_IF_DK_VERY_CLOSE': LEFT_TURN_HARD_IF_DK_VERY_CLOSE,
  'RIGHT_TURN_HARD_IF_L_VERY_CLOSE': RIGHT_TURN_HARD_IF_L_VERY_CLOSE,
  'RIGHT_TURN_HARD_IF_LK_VERY_CLOSE': RIGHT_TURN_HARD_IF_LK_VERY_CLOSE,
  'LEFT_TURN_SOFT_IF_D_CLOSE': LEFT_TURN_SOFT_IF_D_CLOSE,
  'RIGHT_TURN_SOFT_IF_L_CLOSE': RIGHT_TURN_SOFT_IF_L_CLOSE,
  'RIGHT_TURN_HARD_IF_WRONG_WAY': RIGHT_TURN_HARD_IF_WRONG_WAY
}

class HelmFuzzySystem(FuzzySystem):
  def __init__(self, defuzzifier: IDefuzzifier, rules = HELM_RULES_BASE) -> None:
    super().__init__(defuzzifier, rules, FuzzySystemType.MINIMUM)
