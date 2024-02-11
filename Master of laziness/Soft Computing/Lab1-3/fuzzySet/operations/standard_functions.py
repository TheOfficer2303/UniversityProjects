def gamma_function(alpha: float, beta: float):
  def compute(x: int):
    if x < alpha:
      return 0
    if x >= beta:
      return 1

    return (x - alpha) / (beta - alpha)

  return compute

def lambda_function(alpha: float, beta: float, gamma: float):
  def compute(x: int):
    if x < alpha:
      return 0
    if x >= gamma:
      return 0

    if x >= alpha and x < beta:
      return (x - alpha) / (beta - alpha)

    if x >= beta and x < gamma:
      return (gamma - x) / (gamma - beta)

  return compute

def l_function(alpha: float, beta: float):
  def compute(x: int):
    if x < alpha:
      return 1
    if x >= beta:
      return 0

    return (beta - x) / (beta - alpha)

  return compute
