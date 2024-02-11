import copy
from domain.domain import Domain, IDomain
from domain.domainElement import DomainElement
from fuzzySet.fuzzy import IFuzzySet, MutableFuzzySet

def debug_domain(domain: IDomain, heading: str) -> None:
    if heading is not None:
        print(heading)

    for element in domain:
        print(f"Domain Element: {element}")

    print(f"Domain Cardinality: {domain.get_cardinality()}")
    print()

class Relations:
  @staticmethod
  def is_u_times_u_relation(relation: IFuzzySet):
    domain = relation.get_domain()
    if domain.get_number_of_components() == 2:
      domain1 = domain.get_component(0)
      domain2 = domain.get_component(1)

      for i in range(domain1.get_cardinality()):
        if domain1.element_for_index(i) != domain2.element_for_index(i):
          return False

    return True

  @staticmethod
  def is_symmetric(relation: IFuzzySet):
    if not Relations.is_u_times_u_relation(relation):
      return False

    for i in range(relation.get_domain().get_cardinality()):
      element = relation.get_domain().element_for_index(i)
      x = element.get_component_value(0)
      y = element.get_component_value(1)

      if relation.get_value_at(element) != relation.get_value_at(DomainElement.of(y, x)):
        return False

    return True

  @staticmethod
  def is_reflexive(relation: IFuzzySet):
    if not Relations.is_u_times_u_relation(relation):
      return False

    for element in relation.get_domain():
      x = element.get_component_value(0)
      y = element.get_component_value(1)

      if x == y:
        if relation.get_value_at(DomainElement.of(x, x)) != 1:
          return False

    return True

  @staticmethod
  def is_min_max_transitive(relation: IFuzzySet):
    if not Relations.is_u_times_u_relation(relation):
      return False

    for element in copy.copy(relation.get_domain()):
      values = []
      x = element.get_component_value(0)
      z = element.get_component_value(1)

      xz = relation.get_value_at(element)

      for y_element in copy.copy(relation.get_domain().get_component(0)):
        y = y_element.get_component_value(0)

        xy = relation.get_value_at(DomainElement.of(x, y))
        yz = relation.get_value_at(DomainElement.of(y, z))

        values.append(min(xy, yz))

      if xz < max(values):
        return False

    return True

  @staticmethod
  def composition_of_binary_relations(r1: IFuzzySet, r2: IFuzzySet):
    r1 = copy.deepcopy(r1)
    r2 = copy.deepcopy(r2)

    # X x Y i Y x Z
    X = r1.get_domain().get_component(0)
    Y1 = r1.get_domain().get_component(1)
    Y2 = r2.get_domain().get_component(0)
    Z = r2.get_domain().get_component(1)

    domain = Domain.combine(X, Z)
    new_set = MutableFuzzySet(domain)

    for x in X:
      for z in Z:
        mu = []
        for y in Y1:
          value1 = r1.get_value_at(DomainElement.of(x.get_component_value(0), y.get_component_value(0)))
          value2 = r2.get_value_at(DomainElement.of(y.get_component_value(0), z.get_component_value(0)))

          mu.append(min(value1, value2))

        new_set.set_value(DomainElement.of(x.get_component_value(0), z.get_component_value(0)), max(mu))

    return new_set

  @staticmethod
  def is_fuzzy_equivalence(relation: IFuzzySet):
    return Relations.is_symmetric(relation) and Relations.is_reflexive(relation) and Relations.is_min_max_transitive(relation)
