import numpy as np
from pulp import LpBinary, LpMinimize, LpProblem, LpVariable, PULP_CBC_CMD, PULP_CHOCO_CMD, lpSum

def construct_problem(costs):
    workers, jobs = costs.shape

    x = LpVariable.dicts(name="x", indexs=(range(workers), range(jobs)), cat=LpBinary)

    problem = LpProblem(name="Problem pridruzivanja", sense=LpMinimize)

    problem += lpSum(costs[i][j] * x[i][j]
                     for i in range(workers)
                     for j in range(jobs))

    for i in range(workers):
      problem += lpSum(x[i][j] for j in range(jobs)) == 1

    for j in range(jobs):
      problem += lpSum(x[i][j] for i in range(workers)) == 1

    return problem


def solve_LP(problem):
    problem.solve(solver=PULP_CBC_CMD(msg=False))

    return problem


def solve_CP(problem):
    problem.solve(solver=PULP_CHOCO_CMD(msg=False))

    return problem


np.random.seed(3652494221)

mali_costs = np.random.randint(low=1, high=20 + 1, size=(8, 8), dtype=np.int64)
veliki_costs = np.random.randint(low=1, high=20 + 1, size=(16, 16), dtype=np.int64)
