import math
import numpy as np
import numpy.typing as npt

import matplotlib.pyplot as plt

from methods import backward_euler_method, euler_method, predictor_corrector, runge_kutta, trapezoid


def plot_task_solution(task_name, N, euler, b_euler, trapez, runge, pece=None, pece2=None):
  fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)
  euler = np.column_stack(euler)
  b_euler = np.column_stack(b_euler)
  trapez = np.column_stack(trapez)
  runge = np.column_stack(runge)
  pece = np.column_stack(pece)
  pece2 = np.column_stack(pece2)

  ax1.plot(range(N + 1), b_euler[0], label="Backward Euler")
  ax1.plot(range(N + 1), trapez[0], label="Trapezoidal")
  ax1.plot(range(N + 1), euler[0], label="Euler")
  ax1.plot(range(N + 1), runge[0], label="Runge-Kutta")
  # ax1.plot(range(N + 1), pece[0], label="PECE")
  # ax1.plot(range(N + 1), pece2[0], label="PECE2")
  ax1.legend(loc="upper left")

  ax2.plot(range(N + 1), b_euler[1], label="Backward Euler")
  ax2.plot(range(N + 1), trapez[1], label="Trapezoidal")
  ax2.plot(range(N + 1), euler[1], label="Euler")
  ax2.plot(range(N + 1), runge[1], label="Runge-Kutta")
  # ax2.plot(range(N + 1), pece[1], label="PECE")
  # ax2.plot(range(N + 1), pece2[1], label="PECE2")
  ax2.legend()

  plt.savefig(f"tasks/{task_name}.png")

def task1_analytical(N, x0: npt.NDArray[np.float64], T, t_max):
  x1_t0 = x0[0]
  x2_t0 = x0[1]
  time_points = np.linspace(0, t_max, int((t_max - 0) / T))

  x1 = x1_t0 * np.cos(time_points) + x2_t0 * np.sin(time_points)
  x2 = x2_t0 * np.cos(time_points) - x1_t0 * np.sin(time_points)

  return np.column_stack((x1, x2))

def calculate_cumulative_error(numeric_solution: npt.NDArray[np.float64], analytical_solution: npt.NDArray[np.float64]):
  cumulative_error = np.sum(np.abs(numeric_solution - analytical_solution))
  return cumulative_error

def analyze(N: int, x0: npt.NDArray[np.float64], numeric_solution: npt.NDArray[np.float64], analytical, name: str, T, t_max):
  analytical_solution_values = analytical(N, x0, T, t_max)
  cumulative_error = calculate_cumulative_error(numeric_solution, analytical_solution_values)
  print(f"Cumulative error for {name}: {cumulative_error}\n")


def solve(task_name, x0, A, B, T, t_max, r=None):
  N = int(t_max // T)

  numeric_solution_euler = euler_method(x0, A, T, t_max, B=B, r=r)
  analyze(N, x0, numeric_solution_euler, task1_analytical, "Euler", T, t_max)

  numeric_solution_backward_euler = backward_euler_method(x0, A, T, t_max, B=B, r=r)
  analyze(N, x0, numeric_solution_backward_euler, task1_analytical, "Backward Euler", T, t_max)

  ns_trapez = trapezoid(x0, A, T, t_max, B=B, r=r)
  analyze(N, x0, ns_trapez, task1_analytical, "Trapezoid", T, t_max)

  ns_runge = runge_kutta(x0, A, T, t_max, B=B, r=r)
  analyze(N, x0, ns_runge, task1_analytical, "Runge-Kutta", T, t_max)

  pece = predictor_corrector(x0, A, T, t_max, predictor=euler_method, corrector=trapezoid, corr_number=2, B=B, r=r)
  analyze(N, x0, pece, task1_analytical, "PECE", T, t_max)

  # PE(CE)2
  pece2 = predictor_corrector(x0, A, T, t_max, predictor=euler_method, corrector=backward_euler_method, corr_number=2, B=B, r=r)
  analyze(N, x0, pece2, task1_analytical, "PE(CE)^2", T, t_max)

  plot_task_solution(task_name, N, numeric_solution_euler, numeric_solution_backward_euler, ns_trapez, ns_runge, pece=pece, pece2=pece2)

def task1():
  print("# Task 1")
  T = 0.01
  t_max = 10

  A = np.array([
    [0, 1],
    [-1, 0]
  ])
  B = np.array([
    [0, 0],
    [0, 0]
  ])

  # x1 je odmak, x2 je brzina
  x0 = np.array([
    [1],
    [1]
  ])

  solve("Task1", x0, A, B, T, t_max)

def task2():
  print("# Task 2")
  T = 0.1
  t_max = 1

  A = np.array([
    [0, 1],
    [-200, -102]
  ])
  B = np.array([
    [0, 0],
    [0, 0]
  ])

  # x1 je odmak, x2 je brzina
  x0 = np.array([
    [1],
    [-2]
  ])

  solve("Task2", x0, A, B, T, t_max)


def task3():
  print("# Task 3")
  T = 0.01
  t_max = 10

  A = np.array([
    [0, -2],
    [1, -3],
  ])
  B = np.array([
    [2, 0],
    [0, 3],
  ])

  r = lambda _: np.array([
    [1],
    [1],
  ])

  # x1 je odmak, x2 je brzina
  x0 = np.array([
    [1],
    [3]
  ])

  solve("Task3", x0, A, B, T, t_max)

def task4():
  print("# Task 4")
  T = 0.01
  t_max = 1

  A = np.array([
    [1, -5],
    [1, -7],
  ])
  B = np.array([
    [5, 0],
    [0, 3],
  ])

  r = lambda t: np.array([
    [t],
    [t],
  ])

  # x1 je odmak, x2 je brzina
  x0 = np.array([
    [-1],
    [3]
  ])

  solve("Task4", x0, A, B, T, t_max)

def main():
  task1()
  task2()
  task3()
  task4()

if __name__ == "__main__":
  main()
