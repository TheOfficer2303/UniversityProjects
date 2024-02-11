import sys
from rule import InputValues, Rule

from system.defuzzifier.defuzzifier import COADefuzzifier, IDefuzzifier
from system.fuzzy_system.acceleration import ACC_RULES_BASE, AccelerationFuzzySystem
from system.fuzzy_system.fuzzy_system import FuzzySystem
from system.fuzzy_system.helm import HELM_RULES_BASE, HelmFuzzySystem


def test_inputs_on_base():
  defuzzifier: IDefuzzifier = COADefuzzifier()
  helm: FuzzySystem = HelmFuzzySystem(defuzzifier)
  accelerator: FuzzySystem = AccelerationFuzzySystem(defuzzifier)

  L, D, LK, DK, V, S = [int(x) for x in input().split(" ")]
  values = InputValues(L, D, LK, DK, V, S)

  print(accelerator.decide(values), helm.decide(values))

def test_inputs_on_rule():
  defuzzifier: IDefuzzifier = COADefuzzifier()
  print("Input values:")
  L, D, LK, DK, V, S = [int(x) for x in input().split(" ")]
  values = InputValues(L, D, LK, DK, V, S)

  print("Choose one rule:")

  i = 0
  for rule in ACC_RULES_BASE.keys():
    print(f"{i + 1}: {rule}")
    i += 1

  for rule in HELM_RULES_BASE.keys():
    print(f"{i + 1}: {rule}")
    i += 1

  rule_number = int(input())
  rule = {}
  if rule_number >= 1 and rule_number < 5:
    rule[list(ACC_RULES_BASE)[rule_number + 1]] = list(ACC_RULES_BASE.values())[rule_number + 1]
    accelerator = AccelerationFuzzySystem(defuzzifier, rules=rule)
    result = accelerator.decide(values)
  elif rule_number >= 5 and rule_number <= 10:
    rule_number = len(HELM_RULES_BASE) - rule_number
    rule[list(HELM_RULES_BASE)[rule_number + 1]] = list(HELM_RULES_BASE.values())[rule_number + 1]
    helm = HelmFuzzySystem(defuzzifier, rules=rule)
    result = helm.decide(values)
  else:
    raise ValueError("Index out of bounds. Unknown rule.")

  print(result)

def test_simulator():
  defuzzifier: IDefuzzifier = COADefuzzifier()
  helm: FuzzySystem = HelmFuzzySystem(defuzzifier)
  accelerator: FuzzySystem = AccelerationFuzzySystem(defuzzifier)

  while True:
    L, D, LK, DK, V, S = [int(x) for x in input().split(" ")]
    values = InputValues(L, D, LK, DK, V, S)

    print(accelerator.decide(values), helm.decide(values))

    sys.stdout.flush()

def main() -> None:
  # test_inputs_on_base()
  test_simulator()
  # test_inputs_on_rule()


if __name__ == "__main__":
    main()
