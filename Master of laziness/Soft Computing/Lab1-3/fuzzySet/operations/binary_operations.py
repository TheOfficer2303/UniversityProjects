def zadeh_and():
  def compute(value1, value2):
    return min(value1, value2)

  return compute

def zadeh_or():
  def compute(value1, value2):
    return max(value1, value2)

  return compute

def hamacher_t_norm(p: float):
  def compute(a, b):
    return (a * b) / (p + (1 - p) * (a + b - a * b))

  return compute

def hamacher_s_norm(p: float):
  def compute(a, b):
    return (a + b - (2 - p) * a * b) / (1 - (1 - p) * a * b)

  return compute
