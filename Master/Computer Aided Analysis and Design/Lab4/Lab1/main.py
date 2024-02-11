from copy import deepcopy
from matrix import Matrix

def save_to_file(file: str, matrix: Matrix):
  with open(file, "w") as file:
    file.writelines(str(matrix))

def task1():
  task_name = f"task1"
  print(task_name)

  a = Matrix(file=f"{task_name}/A.txt")
  b = Matrix(file=f"{task_name}/A.txt")

  print(f"Matrix A before operations:\n{a}")
  assert a == b

  a *= (0.5)
  a *= 1/0.5

  print(f"Matrix A after operations:\n{a}")
  save_to_file(f"{task_name}/output.txt", a)

def task2_6(number):
  task_name = f"task{number}"
  print(task_name)

  A = Matrix(file=f"{task_name}/A.txt")
  b = Matrix(file=f"{task_name}/b.txt")

  lu_solution = A.lu_solve(b)
  lup_solution = A.lup_solve(b)

  print(f"LU solution:\n{lu_solution}")
  print(f"LUP solution:\n{lup_solution}")
  print()

  save_to_file(f"{task_name}/lu.txt", lu_solution)
  save_to_file(f"{task_name}/lup.txt", lup_solution)

def task7_8(number: int):
  task_name = f"task{number}"
  print(task_name)

  A = Matrix(file=f"{task_name}/A.txt")
  A_inverse = A.inverse()

  print(f"A-1:\n{A_inverse}")
  print()

  save_to_file(f"{task_name}/inverse.txt", A_inverse)

def task9_10(number: int):
  task_name = f"task{number}"
  print(task_name)

  A = Matrix(file=f"{task_name}/A.txt")
  det_A = A.determinant()

  print(f"det(A):\n{det_A}")
  print()

  save_to_file(f"{task_name}/det.txt", det_A)

def main():
  task1()

  for i in range(2, 7):
    task2_6(i)

  for i in range(7, 9):
    task7_8(i)

  for i in range(9, 11):
    task9_10(i)

if __name__ == "__main__":
  main()
