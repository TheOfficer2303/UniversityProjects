class DomainElement:
  def __init__(self, values):
    self.values = values

  def get_number_of_components(self):
    return len(self.values)

  def get_component_value(self, index: int):
    if index < 0 or index >= self.get_number_of_components():
      raise IndexError("Index must be larger than 0 and in range")
    return self.values[index]

  @staticmethod
  def of(*values: int):
    return DomainElement(values)

  def __eq__(self, obj):
    return isinstance(obj, DomainElement) and obj.values == self.values

  def __hash__(self):
    return hash(tuple(self.values))

  def __repr__(self):
    return f"{self.values}"
