class Person:
  def __init__(self, name, age):
      self.name = name
      self.age = age

  def increase_age(self):
    self.age += 1

class PersonDetail(Person):
  def __init__(self, name, age, address):
    super().__init__(name, age)
    self.address = address


first_person = Person('Marko', 39)
second_person = Person('Ivan', 17)

second_person.increase_age()

first_person_detail = PersonDetail('Ana', 25, 'Unska 3')
first_person_detail.increase_age()

# Definirajte varijable first_person i second_person kao instance klase Person s vrijednostima Marko, 39 i Ivan, 17.
# Vrijednosti predajte preko konstruktora.

# Pozovite metodu increase_age nad instancom second_person.

# Definirajte klasu PersonDetail koja nasljeđuje klasu Person.
# Pritom u klasi PersonDetail definirajte atribut address koji se uz nasljeđene atribute postavlje preko konstruktora.

# Definirajte varijablu first_person_detail kao instancu klase PersonDetail s vrijednostima Ana, 25, Unska 3.

# Nad varijablom first_person_detail pozovite metodu increase_age.
