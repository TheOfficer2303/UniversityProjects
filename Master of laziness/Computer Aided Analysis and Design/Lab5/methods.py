import numpy as np
import numpy.typing as npt
from scipy.linalg import solve

def euler_method(x0: npt.NDArray[np.float64], A: npt.NDArray[np.float64], T: float, t_max: int, B=None, r=None, predictor=False, i=None):
  if predictor:
    if r is not None:
      return x0 + T * (np.dot(A, x0) + np.dot(B, r(i * T)))

    return x0 + T * A.dot(x0)

  N = int(t_max // T)
  x = [x0]

  for i in range(N):
    if r is not None:
      x_next = x[i] + T * (A.dot(x[i]) + B.dot(r(i * T)))
    else:
      x_next = x[i] + T * A.dot(x[i])
    x.append(x_next)

  return np.array(x).squeeze()

def backward_euler_method(x0: npt.NDArray[np.float64], A: npt.NDArray[np.float64], T: float, t_max: int, B=None, r=None, corrector=False, x_next=None, i=None):
  if corrector:
    if r is not None:
      return x0 + T * (A.dot(x_next) + B.dot(r((i + 1) * T)))

    return x0 + T * A.dot(x_next)

  N = int(t_max // T)
  x = [x0]

  # X(k+1) = X(k) + Tx'
  # X(k+1) = X(k) + T A X (k+1)
  # (I - TA) X(k+1) = X(k) -> rijesi za X(k+1), u ovom slucaju x[i + 1]
  P = np.eye(len(x0)) - A.dot(T)


  for i in range(N):
    if r is not None:
      x.append(solve(P, x[i] + T * B.dot(r((i + 1) * T))))
    else:
      x.append(solve(P, x[i]))

  return np.array(x).squeeze()

def trapezoid(x0: npt.NDArray[np.float64], A: npt.NDArray[np.float64], T: float, t_max: int, B=None, r=None, corrector=False, x_next=None, i=None):
  if corrector:
    if r is not None:
      return x0 + T / 2 * ((A.dot(x0) + B.dot(r(i))) + A.dot(x_next) + B.dot(r(i * T)))
    return x0 + T / 2 * (A.dot(x0) + A.dot(x_next))

  N = int(t_max // T)
  x = [x0]

  I = np.eye(len(x0))
  system_matrix = I - 0.5 * T * A

  for i in range(N):
    if r is not None:
      rhs = (I + 0.5 * T * A).dot(x[i]) + (0.5 * T * B).dot(r(i) + r(i + 1))
    else:
      rhs = (I + 0.5 * T * A).dot(x[i])

    solution = solve(system_matrix, rhs)

    x.append(solution)

  return np.array(x).squeeze()

def runge_kutta(x0: npt.NDArray[np.float64], A: npt.NDArray[np.float64], T: float, t_max: int, B=None, r=None):
  N = int(t_max // T)
  x = [x0]

  for i in range(N):
    if r is not None:
      t = i * T
      m1 = A.dot(x[i]) + B.dot(r(t))
      m2 = A.dot(x[i] + 0.5 * T * m1) + B.dot(r(t + 0.5 * T))
      m3 = A.dot(x[i] + 0.5 * T * m2) + B.dot(r(t + 0.5 * T))
      m4 = A.dot(x[i] + T * m3) + B.dot(r(t + T))
    else:
      m1 = A.dot(x[i])
      m2 = A.dot(x[i] + 0.5 * T * m1)
      m3 = A.dot(x[i] + 0.5 * T * m2)
      m4 = A.dot(x[i]+ T * m3)

    x.append(x[i] + T / 6 * (m1 + 2 * m2 + 2 * m3 + m4))

  return np.array(x).squeeze()

def predictor_corrector(x0: npt.NDArray[np.float64], A: npt.NDArray[np.float64], T: float, t_max: int, predictor, corrector, corr_number, B=None, r=None):
  N = int(t_max // T)
  x = [x0]

  for i in range(N):
    value = predictor(x[i], A, 1, 1, B, r, predictor=True, i=i)
    for _ in range(corr_number):
      value = corrector(x[i], A, 1, 1, B, r, corrector=True, x_next=value, i=i)

    x.append(value)

  return np.array(x).squeeze()
