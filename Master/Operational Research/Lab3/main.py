from pulp import LpVariable, LpMaximize, LpProblem, lpSum, LpInteger

def construct_LP_equivalent():
  problem = LpProblem("robust_LP", LpMaximize)

  x1 = LpVariable("x1", lowBound=0, upBound=4, cat=LpInteger)
  x2 = LpVariable("x2", lowBound=0, upBound=6, cat=LpInteger)

  constraints = {
    "x1": x1,
    "x2": x2
  }

  problem += 3 * x1 + 5 * x2

  ud = 4
  p1 = LpVariable.dicts(name="p1", indexs=range(ud), lowBound=0)
  d = [0, 2, -4, 6]
  d1 = [[-1, 1], [1, -1], [-1, -1], [1, 1]]

  problem += lpSum([p1[i] * d[i] for i in range(len(d))]) <= 18
  problem += lpSum([p1[i] * d1[i][0] for i in range(len(d1))]) == x1
  problem += lpSum([p1[i] * d1[i][1] for i in range(len(d1))]) == x2

  return problem, constraints


