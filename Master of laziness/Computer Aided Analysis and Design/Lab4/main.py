from Lab3.functions.f2 import f2
from Lab3.functions.f1 import f1
from Lab3.functions.function import Function, Point
from functions.f4 import f4
from methods.box import box
from methods.mixed import mixed

def constraint_1(x: Point):
  x1 = x[0]
  x2 = x[1]

  return x2 - x1

def constraint_2(x: Point):
  x1 = x[0]

  return 2 - x1

def constraint_3(x: Point):
  x1 = x[0]
  x2 = x[1]

  return 3 - x1 - x2

def constraint_4(x: Point):
  x1 = x[0]
  x2 = x[1]

  return 3 + 1.5 * x1 - x2

def constraint_5(x: Point):
  x2 = x[1]

  return x2 - 1

def task1():
  print("#task 1")
  f_1 = Function("Function 1", f1)
  f_2 = Function("Function 2", f2)
  x0: Point = [-1.9, 2]


  minimum = box(f_1, x0, -100, 100, (constraint_1, constraint_2))
  if minimum is not None:
    print(f"{f_1.name} s ograničenjima:")
    print(f"x0={x0}, Minimum: {minimum}, Min vrijednost: {f_1.evaluate(minimum)}")

  f_1.reset()
  while True:
    minimum = box(f_1, x0)
    if minimum is not None:
      print(f"{f_1.name} bez ograničenja:")
      print(f"x0={x0}, Minimum: {minimum}, Min vrijednost: {f_1.evaluate(minimum)}")
      break

  x0: Point = (0.1, 0.3)
  minimum = box(f_2, x0, -100, 100, (constraint_1, constraint_2))
  if minimum is not None:
    print(f"{f_2.name} s ograničenjima:")
    print(f"x0={x0}, Minimum: {minimum}, Min vrijednost: {f_2.evaluate(minimum)}")

  f_2.reset()
  minimum = box(f_2, x0)
  if minimum is not None:
    print(f"{f_2.name} bez ograničenja:")
    print(f"x0={x0}, Minimum: {minimum}, Min vrijednost: {f_2.evaluate(minimum)}")

  print()

def task2():
  print("#task 2")
  f = Function("Function 1", f1)
  x0: Point = [-1.9, 2]

  minimum = mixed(f, x0, g=(constraint_1, constraint_2))
  print(f"{f.name}, x0={x0}, Minimum u tocki {minimum} s vrijednosti {f.evaluate(minimum)}")

  x0: Point = [0.2, 2.5]
  minimum = mixed(f, x0, g=(constraint_1, constraint_2))
  print(f"{f.name}, x0={x0}, Minimum u tocki {minimum} s vrijednosti {f.evaluate(minimum)}")


  x0: Point = [0.1, 0.3]
  f = Function("Function 2", f2)
  minimum = mixed(f, x0, g=(constraint_1, constraint_2))
  print(f"{f.name}, x0={x0}, Minimum u tocki {minimum} s vrijednosti {f.evaluate(minimum)}")

  print()

def task3():
  print("#task 3")
  f = Function("Function 4", f4)
  x0: Point = [5.0, 5.0]

  minimum = mixed(f, x0, g=(constraint_3, constraint_4, constraint_5))
  print(f"{f.name}, x0={x0}, Minimum u tocki {minimum} s vrijednosti {f.evaluate(minimum)}")

  x0: Point = [0.0, 1.0]
  minimum = mixed(f, x0, g=(constraint_3, constraint_4))
  print(f"{f.name}, x0={x0}, Minimum u tocki {minimum} s vrijednosti {f.evaluate(minimum)}")

  print()

def main():
  # task1()
  task2()
  # task3()

if __name__ == '__main__':
  main()
