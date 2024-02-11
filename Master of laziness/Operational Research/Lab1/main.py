from matplotlib import pyplot as plt
from pulp import LpProblem, LpMaximize, LpVariable, LpInteger, LpMinimize
import numpy as np
import pulp

def primal():
  problem = LpProblem("maximise_profit", LpMaximize)

  p1 = LpVariable("p1", 0, None, LpInteger) # proizvod P1
  p2 = LpVariable("p2", 0, None, LpInteger) # proizvod P2

  problem += 30 * p1 + 50 * p2 # funkcija cilja

  problem += 5 * p1 + 6 * p2 <= 1500 # ogranicenje stroja 1
  problem += 7.5 * p1 + 4 * p2 <= 1500 # ogranicenje stroja 2
  problem += (3 + 1/3) * p1 + 9 * p2 <= 1600 # ogranicenje stroja 3

  problem.solve()
  print("Status rješenja:", pulp.LpStatus[problem.status])
  print("Optimalna proizvodnja proizvoda P1:", p1.varValue)
  print("Optimalna proizvodnja proizvoda P2:", p2.varValue)
  print("Maksimalna dobit:", pulp.value(problem.objective))

def dual():
  dual_problem = LpProblem("Dual_Problem", LpMinimize)

  y1 = LpVariable("s1", 0) # strojevi S1
  y2 = LpVariable("s2", 0) # strojevi S2
  y3 = LpVariable("s3", 0) # strojevi S3

  dual_problem += 1500 * y1 + 1500 * y2 + 1600 * y3 # funkcija cilja

  dual_problem += 5 * y1 + 7.5 * y2 + 3.33 * y3 >= 30 # proizvod P1
  dual_problem += 6 * y1 + 4 * y2 + 9 * y3 >= 50 # proizvod P1

  dual_problem.solve()
  for machine in dual_problem.variables():
    print(machine.name, ":", machine.varValue)

def plot():

  x = np.linspace(0, 200, 100)
  y = np.linspace(0, 200, 100)
  x, y = np.meshgrid(x, y)

  c1 = (1500 - 5 * x - 6 * y)
  c2 = (1500 - 7.5 * x - 4 * y)
  c3 = (1600 - 3.33 * x - 9 * y)

  fig = plt.figure()
  ax = fig.add_subplot(111, projection="3d")

  ax.plot_surface(x, y, c1, alpha=0.5, label="5x1 + 6x2 <= 1500")
  ax.plot_surface(x, y, c2, alpha=0.5, label="7.5x1 + 4x2 <= 1500")
  ax.plot_surface(x, y, c3, alpha=0.5, label="3.33x1 + 9x2 <= 1600")

  ax.scatter(0, 200, 100, color='red', s=50, label='Optimal solution (x1=131, x2=129)')

  ax.set_xlabel("x1")
  ax.set_ylabel("x2")
  ax.set_zlabel("x3")
  ax.legend()

  plt.show()


def main():
  primal()
  dual()
  plot()


if __name__ == "__main__":
    main()
