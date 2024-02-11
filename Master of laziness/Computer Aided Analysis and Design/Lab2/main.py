import random
from math import sqrt, sin, fabs

from tabulate import tabulate
from methods.coordinated_search import coordinate_search
from methods.hooke_jeeves import hooke_jeeves
from point import Function, Point
from methods.golden_ratio import golden_ratio
from methods.simplex import nelder_mead_simplex

def task1_Function(x: int | Point):
  if not (isinstance(x, float) or isinstance(x, int)):
    x = x[0]

  return (x - 3)**2

def f1(x: Point):
  if len(x) != 2:
    raise ValueError("Function is 2d")

  x1 = x[0]
  x2 = x[1]

  return 100 * (x2 - x1**2)**2 + (1 - x1)**2


def f2(x: Point):
  if len(x) != 2:
    raise ValueError("Function is 2d")

  x1 = x[0]
  x2 = x[1]

  return (x1 - 4)**2 + 4 * ((x2 - 2)**2)


def f3(x: Point):
  sum = 0

  for i in range(len(x)):
    sum += (x[i] - i) ** 2

  return sum


def f4(x: Point):
  if len(x) != 2:
    raise ValueError("Function is 2d")

  x1 = x[0]
  x2 = x[1]

  return fabs((x1 - x2) * (x1 + x2)) + sqrt(x1**2 + x2**2)

def f6(x: Point):
  xi_squared_sum = 0

  for i in range(len(x)):
    xi_squared_sum += x[i]**2

  numerator = (sin(sqrt(xi_squared_sum)))**2 - 0.5
  denominator = (1 + 0.001 * xi_squared_sum) ** 2

  return 0.5 + numerator / denominator

def task1():
  print("# task1")
  f = Function("Task1 function", task1_Function)

  print_output([10], function=f)
  print_output([20], function=f)
  print_output([50], function=f)
  print_output([100], function=f)


def task2():
  print("# task2")
  func1 = Function("Function f1", f1)
  x0: Point = [-1.9, 2]
  outputs1 = print_output(x0, func1)

  func2 = Function("Function f2", f2)
  x0: Point = [0.1, 0.3]
  outputs2 = print_output(x0, func2)

  func3 = Function("Function f3", f3)
  x0: Point = [0, 0, 0, 0, 0, 0]
  outputs3 = print_output(x0, func3)

  func4 = Function("Function f4", f4)
  x0: Point = [5.1, 1.1]
  outputs4 = print_output(x0, func4)

  table_data = list(zip(['Coordinate search', 'Hooks-Jeeves', 'Nelder-Mead'], outputs1, outputs2, outputs3, outputs4))

  # Define table headers
  headers = ["Func 1", "Func 2", "Func 3", "Func 4"]
  print(tabulate(table_data, headers=headers, tablefmt='grid'))

def task3():
  print("# task3")
  func4 = Function("Function f4", f4)
  x0: Point = [5, 5]

  print_output(x0, function=func4, coord=False)

def task4():
  print("# task4")
  func = Function("Function f1", f1)
  x0: Point = [0.5, 0.5]

  print("Point: (0.5, 0.5)")
  for i in range(1, 20):
    simplex_result = nelder_mead_simplex(func, x0, step=i)
    print(f"Simplex search:\nMinimum - {simplex_result}\nIterations - {func.count}\nStep={i}\n")
    func.reset()

  print("\n\n")

  x0: Point = [20, 20]

  print("Point: (20, 20)")
  for i in range(1, 20):
    simplex_result = nelder_mead_simplex(func, x0, step=i)
    print(f"Simplex search:\nMinimum - {simplex_result}\nIterations - {func.count}\nStep={i}")
    func.reset()

def task5():
  print("# task5")

  func = Function("Function 6", f6)

  i = 1
  while True:
    x0 = [random.uniform(-50.0, 50.0) for _ in range(2)]
    res = nelder_mead_simplex(func, x0)

    e = 10e-4
    if abs(func.evaluate(res)) < e:
      print(f"Nelder-Mead (x0={x0}):\nMinimum - {res}\nIterations - {func.count}\nf(minimum)={func.evaluate(res)}\n")
      func.reset()
      print(f"Found solution after generating {i} random points")
      break
    i += 1


def print_output(x0, function: Function, coord = True, hooke = True, simplex = True):
  print(f"## {function.name}")
  if (len(x0) == 1):
    golden_ratio_result = golden_ratio(function, x0=x0[0])
    print(f"Golden ratio search:\nMinimum - {golden_ratio_result}\nIterations - {function.count}\n")
    function.reset()

  if coord:
    coordinate_search_result = coordinate_search(function, x0=x0)
    count2 = function.count
    print(f"Coordinate search:\nMinimum - {coordinate_search_result}\nIterations - {count2}\n")
    function.reset()

  if hooke:
    hooke_jeeves_result = hooke_jeeves(function, x0=x0)
    count3 = function.count
    print(f"Hooke-Jeeves search:\nMinimum - {hooke_jeeves_result}\nIterations - {count3}\n")
    function.reset()

  if simplex:
    simplex_result = nelder_mead_simplex(function, x0)
    count4 = function.count
    print(f"Simplex search:\nMinimum - {simplex_result}\nIterations - {count4}\n")
    function.reset()

  return count2, count3, count4

def main():
  task1()
  # task2()
  # task3()
  # task4()
  # task5()

if __name__ == '__main__':
  main()
