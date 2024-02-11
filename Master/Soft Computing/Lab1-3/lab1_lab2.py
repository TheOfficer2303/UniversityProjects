from domain.domain import Domain, IDomain
from domain.domainElement import DomainElement
from fuzzySet.fuzzy import CalculatedFuzzySet, IFuzzySet, MutableFuzzySet
from fuzzySet.operations.binary_operations import hamacher_t_norm, zadeh_or
from fuzzySet.operations.operation_types import Operations
from fuzzySet.operations.standard_functions import lambda_function
from fuzzySet.operations.unary_operations import zadeh_not
from relations.relations import Relations

def debug_domain(domain: IDomain, heading: str) -> None:
    if heading is not None:
        print(heading)

    for element in domain:
        print(f"Domain Element: {element}")

    print(f"Domain Cardinality: {domain.get_cardinality()}")
    print()

def debug_set(fuzzy_set: MutableFuzzySet, heading: str):
    if heading is not None:
        print(heading)

    for element in fuzzy_set.get_domain():
        print(f"d({element})={fuzzy_set.get_value_at(element):.6f}")


    print()

def test_domain():
  d1: IDomain = Domain.int_range(0, 5)
  debug_domain(d1, "Elements of Domain 1:")

  d2: IDomain = Domain.int_range(0, 3)
  debug_domain(d2, "Elements of Domain 2:")

  d3: IDomain = Domain.combine(d1, d2)
  debug_domain(d3, "Elements of Domain 3:")

  print(d3.element_for_index(0))
  print(d3.element_for_index(5))
  print(d3.element_for_index(14))
  print(d3.index_of_element(DomainElement.of(4, 1)))
  print()

def test_sets():
    d: IDomain = Domain.int_range(0, 11)
    set1 = (MutableFuzzySet(d)
        .set_value(DomainElement.of(0), 1.0)
        .set_value(DomainElement.of(1), 0.8)
        .set_value(DomainElement.of(2), 0.6)
        .set_value(DomainElement.of(3), 0.4)
        .set_value(DomainElement.of(4), 0.2))

    debug_set(set1, "Set 1:")

    d2: IDomain = Domain.int_range(-5, 6)
    function = lambda_function(
        d2.index_of_element(DomainElement.of(-4)),
        d2.index_of_element(DomainElement.of( 0)),
        d2.index_of_element(DomainElement.of( 4))
    )
    set2 = (CalculatedFuzzySet(d2, function))

    debug_set(set2, "Set 2:")

    not_set1: IFuzzySet =  Operations.unary_operation(set1, zadeh_not())
    debug_set(not_set1, "Not-Set 1:")

    union: IFuzzySet = Operations.binary_operation(set1, not_set1, zadeh_or());
    debug_set(union, "Set1 union notSet1:")

    hinters: IFuzzySet = Operations.binary_operation(set1, not_set1, hamacher_t_norm(1.0))
    debug_set(hinters, "Set1 intersection with notSet1 using parameterised Hamacher T norm with parameter 1.0:")


def test_relations():
    u = Domain.int_range(1, 6)
    u2 = Domain.combine(u, u)

    r1 = (MutableFuzzySet(u2)
        .set_value(DomainElement.of(1,1), 1)
        .set_value(DomainElement.of(2,2), 1)
        .set_value(DomainElement.of(3,3), 1)
        .set_value(DomainElement.of(4,4), 1)
        .set_value(DomainElement.of(5,5), 1)
        .set_value(DomainElement.of(3,1), 0.5)
        .set_value(DomainElement.of(1,3), 0.5))

    r2 = (MutableFuzzySet(u2)
        .set_value(DomainElement.of(1,1), 1)
        .set_value(DomainElement.of(2,2), 1)
        .set_value(DomainElement.of(3,3), 1)
        .set_value(DomainElement.of(4,4), 1)
        .set_value(DomainElement.of(5,5), 1)
        .set_value(DomainElement.of(3,1), 0.5)
        .set_value(DomainElement.of(1,3), 0.1))

    r3 = (MutableFuzzySet(u2)
        .set_value(DomainElement.of(1,1), 1)
        .set_value(DomainElement.of(2,2), 1)
        .set_value(DomainElement.of(3,3), 0.3)
        .set_value(DomainElement.of(4,4), 1)
        .set_value(DomainElement.of(5,5), 1)
        .set_value(DomainElement.of(1,2), 0.6)
        .set_value(DomainElement.of(2,1), 0.6)
        .set_value(DomainElement.of(2,3), 0.7)
        .set_value(DomainElement.of(3,2), 0.7)
        .set_value(DomainElement.of(3,1), 0.5)
        .set_value(DomainElement.of(1,3), 0.5));

    r4 =  (MutableFuzzySet(u2)
        .set_value(DomainElement.of(1,1), 1)
        .set_value(DomainElement.of(2,2), 1)
        .set_value(DomainElement.of(3,3), 1)
        .set_value(DomainElement.of(4,4), 1)
        .set_value(DomainElement.of(5,5), 1)
        .set_value(DomainElement.of(1,2), 0.4)
        .set_value(DomainElement.of(2,1), 0.4)
        .set_value(DomainElement.of(2,3), 0.5)
        .set_value(DomainElement.of(3,2), 0.5)
        .set_value(DomainElement.of(1,3), 0.4)
        .set_value(DomainElement.of(3,1), 0.4));

    test1 = Relations.is_u_times_u_relation(r1)
    print("r1 UxU?", test1)

    test2 = Relations.is_symmetric(r1)
    print("r1 simetricna?: ", test2)

    test3 = Relations.is_symmetric(r2)
    print("Is r2 simmetric: ", test3)

    test4 = Relations.is_reflexive(r2);
    print("r1 je refleksivna? ", test4);

    test5 = Relations.is_reflexive(r3);
    print("r3 je refleksivna? ", test5);

    test6 = Relations.is_min_max_transitive(r3)
    print("r3 je min max trans? ", test6);

    test7 = Relations.is_min_max_transitive(r4)
    print("r4 je min max trans? ", test7);

def test_composition():
    u1 = Domain.int_range(1, 5)
    u2 = Domain.int_range(1, 4)
    u3 = Domain.int_range(1, 5)

    r1 = (MutableFuzzySet(Domain.combine(u1, u2))
        .set_value(DomainElement.of(1,1), 0.3)
        .set_value(DomainElement.of(1,2), 1)
        .set_value(DomainElement.of(3,3), 0.5)
        .set_value(DomainElement.of(4,3), 0.5));

    r2 = (MutableFuzzySet(Domain.combine(u2, u3))
        .set_value(DomainElement.of(1,1), 1)
        .set_value(DomainElement.of(2,1), 0.5)
        .set_value(DomainElement.of(2,2), 0.7)
        .set_value(DomainElement.of(3,3), 1)
        .set_value(DomainElement.of(3,4), 0.4))

    r1r2 = Relations.composition_of_binary_relations(r1, r2)

    for element in r1r2.get_domain():
        print(f"mu({element})={r1r2.get_value_at(element)}")

def test_fuzzy_equivalance():
    u = Domain.int_range(1, 5);

    r = (MutableFuzzySet(Domain.combine(u, u))
        .set_value(DomainElement.of(1,1), 1)
        .set_value(DomainElement.of(2,2), 1)
        .set_value(DomainElement.of(3,3), 1)
        .set_value(DomainElement.of(4,4), 1)
        .set_value(DomainElement.of(1,2), 0.3)
        .set_value(DomainElement.of(2,1), 0.3)
        .set_value(DomainElement.of(2,3), 0.5)
        .set_value(DomainElement.of(3,2), 0.5)
        .set_value(DomainElement.of(3,4), 0.2)
        .set_value(DomainElement.of(4,3), 0.2))

    r2 = r

    print("Početna relacija je neizrazita relacija ekvivalencije? ", Relations.is_fuzzy_equivalence(r2))

    for i in range(3):
        r2 = Relations.composition_of_binary_relations(r2, r)
        print(f"Broj odrađenih kompozicija: {i + 1}. Relacija je:")

        for element in r2.get_domain():
            print(f"mu({element})={r2.get_value_at(element)}")

        print("Ova relacija je neizrazita relacija ekvivalencije?", Relations.is_fuzzy_equivalence(r2))

def main():
    #Lab1
    # test_domain()
    # test_sets()

    #Lab2
    test_relations()
    test_composition()
    test_fuzzy_equivalance()

if __name__ == "__main__":
    main()
