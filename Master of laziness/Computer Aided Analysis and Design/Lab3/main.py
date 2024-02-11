import math
from Lab1.matrix import Matrix
from functions.f1 import f1, f1_G, f1_gradient, f1_hessian, f1_jacobian
from functions.f2 import f2, f2_gradient, f2_hessian
from functions.f3 import f3, f3_gradient, f3_hessian
from functions.f4 import f4, f4_gradient, f4_hessian

from functions.function import Function, Point
from methods.gauss import gauss_newton
from methods.gradient import gradient_descent

def task1():
  print("# task1")
  x0: Point = [0, 0]

  f = Function("Function 3", f3, f3_gradient, f3_hessian)

  result = gradient_descent(f, x0)
  print("Uz odredjivanje optimalnog koraka: ", result)
  print(f"Broj izvodjenja: {f.count}\nBroj racunanja gradijenta: {f.gradient_count}")
  print(f"Vrijednost f.je u tocki: {f.evaluate(result)}\n")
  f.reset()

  result = gradient_descent(f, x0, use_golden_ratio=False)
  print("Bez odredjivanja optimalnog koraka: ", result)
  f.reset()

  print()

def task2():
  print("# task2")
  x0_1: Point = [-1.9, 2]
  x0_2: Point = [0.1, 0.3]

  f_1 = Function("Function 1", f1, f1_gradient, f1_hessian)
  f_2 = Function("Function 2", f2, f2_gradient, f2_hessian)

  print("GRADIJENTNI SPUST")

  f_1.reset()
  result = gradient_descent(f_1, x0_1)
  print(f"{f_1.name}", result)
  print(f"Broj izvodjenja: {f_1.count}\nBroj racunanja gradijenta: {f_1.gradient_count}")
  print(f"Vrijednost f.je u tocki: {f_1.evaluate(result)}\n")
  f_1.reset()

  f_2.reset()
  result = gradient_descent(f_2, x0_2)
  print(f"{f_2.name}", result)
  print(f"Broj izvodjenja: {f_2.count}\nBroj racunanja gradijenta: {f_2.gradient_count}")
  print(f"Vrijednost f.je u tocki: {f_2.evaluate(result)}\n")
  f_2.reset()

  print("NEWTON-RAPSHON")
  f_1.reset()
  result = gradient_descent(f_1, x0_1, newton_method=True)
  print(f"{f_1.name}", result)
  print(f"Broj izvodjenja: {f_1.count}\nBroj racunanja gradijenta: {f_1.gradient_count}\nBroj racunanja Hessea: {f_1.hessian_count}")
  print(f"Vrijednost f.je u tocki: {f_1.evaluate(result)}\n")
  f_1.reset()

  result = gradient_descent(f_2, x0_2, newton_method=True)
  print(f"{f_2.name}", result)
  print(f"Broj izvodjenja: {f_2.count}\nBroj racunanja gradijenta: {f_2.gradient_count}\nBroj racunanja Hessea: {f_2.hessian_count}")
  print(f"Vrijednost f.je u tocki: {f_2.evaluate(result)}\n")
  f_2.reset()

  print()

def task3():
  print("# task3")
  x0_1: Point = [3, 3]
  x0_2: Point = [1, 2]

  f = Function("Function 4", f4, f4_gradient, f4_hessian)

  f.reset()
  x1 = gradient_descent(f, x0_1, newton_method=True)
  print(f"Broj izvodjenja: {f.count}\nBroj racunanja gradijenta: {f.gradient_count}\nBroj racunanja Hessea: {f.hessian_count}")
  print(x1)
  print()

  f.reset()
  x1 = gradient_descent(f, x0_1, newton_method=True, use_golden_ratio=False)
  print(f"Broj izvodjenja: {f.count}\nBroj racunanja gradijenta: {f.gradient_count}\nBroj racunanja Hessea: {f.hessian_count}")
  print(x1)
  print()
  f.reset()

  f.reset()
  x1 = gradient_descent(f, x0_2, newton_method=True)
  print(f"Broj izvodjenja: {f.count}\nBroj racunanja gradijenta: {f.gradient_count}\nBroj racunanja Hessea: {f.hessian_count}")
  print(x1)
  print()

  f.reset()
  x1 = gradient_descent(f, x0_2, newton_method=True, use_golden_ratio=False)
  print(f"Broj izvodjenja: {f.count}\nBroj racunanja gradijenta: {f.gradient_count}\nBroj racunanja Hessea: {f.hessian_count}")
  print(x1)
  print()
  f.reset()

  print()

def task4():
  print("# task4")
  f = Function("Funkcija 1", function=f1, jacobian=f1_jacobian, G=f1_G)
  x0 = [-1.9, 2]

  print(gauss_newton(x0, f=f))
  print(f"Broj izvodjenja: {f.count}\nBroj racunanja gradijenta: {f.gradient_count}\nBroj racunanja Hessea: {f.hessian_count}")

  print()

def task5_jacobian(x: Point) -> Matrix:
  x1 = x[0]
  x2 = x[1]

  return Matrix(elements=[
    [2*x1, 2*x2],
    [-2*x1, 1]
  ])

def task5_G(x: Point) -> Matrix:
  x1 = x[0]
  x2 = x[1]

  return Matrix(elements=[
    [x1**2 + x2**2 - 1],
    [x2 - x1**2]
  ])

def task5():
  print("# task5")
  x1: Point = [2, 2]
  x2: Point = [-2, 2]

  print(f"Pocetna tocka: {x1}, rezultat: {gauss_newton(x1, jacobian_0=task5_jacobian, G_0=task5_G)}\n")
  print(f"Pocetna tocka: {x2}, rezultat: {gauss_newton(x2, jacobian_0=task5_jacobian, G_0=task5_G)}\n")

  print()

def task6_jacobian(x: Point) -> Matrix:
  x1 = x[0]
  x2 = x[1]
  x3 = x[2]

  elements = [[math.exp(coef * x2), coef * x1 * math.exp(coef * x2), 1] for coef in [1, 2, 3, 5, 6, 7]]
  return Matrix(elements=elements)


def task6_G(x: Point) -> Matrix:
  x1 = x[0]
  x2 = x[1]
  x3 = x[2]

  measurements = [(1,3), (2,4), (3,4), (5,5), (6,6), (7,8)]
  elements = []

  for m in measurements:
    t_i = m[0]
    y_i = m[1]
    elements.append([x1 * math.exp(x2 * t_i) + x3 - y_i])

  return Matrix(elements=elements)

def task6():
  print("# task6")

  x0 = [1, 1, 1]
  print(gauss_newton(x0, jacobian_0=task6_jacobian, G_0=task6_G))

  print()


def main():
  task1()
  task2()
  task3()
  task4()
  task5()
  task6()

if __name__ == '__main__':
  main()
