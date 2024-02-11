from __future__ import annotations

from typing import List, Tuple
import copy

EPSILON = 10e-9


class Matrix:
  def __init__(self, row_count: int = None, column_count: int = None, file: str = None, elements: List[List[float]] = None) -> None:
    self.row_count = row_count
    self.column_count = column_count
    self.file = file
    self.elements: List[List[float]] = None
    self.A = None
    self.P = None
    self.row_swap_count = None

    if file is not None:
      self._init_from_file()
      return

    if row_count is not None and column_count is not None:
      self._init_empty()
      return

    if elements is not None:
      self.row_count = len(elements)
      self.column_count = len(elements[0])
      self._init_from_elements(elements)
      return

    row_count, column_count = 0, 0
    self._init_empty()

  def __getitem__(self, indices: Tuple[int, int]):
    if isinstance(indices, int) and not (indices < 0 or indices >= self.row_count):
      return self.elements[indices][0]

    i = indices[0]
    j = indices[1]

    if i < 0 or i >= self.row_count or j < 0 or j >= self.column_count:
      raise ValueError("out of range")

    return self.elements[i][j]

  def __setitem__(self, indices: Tuple[int, int], value: float):
    if isinstance(indices, int) and not (indices < 0 or indices >= self.row_count):
      self.elements[indices][0] = value
      return

    i = indices[0]
    j = indices[1]

    if i < 0 or i >= self.row_count or j < 0 or j >= self.column_count:
      raise ValueError("out of range")

    self.elements[i][j] = value


  def __add__(self: Matrix, other: Matrix):
    if not isinstance(self, Matrix) or not isinstance(other, Matrix):
       raise ValueError("elements must be matrices")

    if self.row_count != other.row_count or self.column_count != other.column_count:
       raise ValueError("Matrices must be of the same dimensions!")

    added_matrix = Matrix(row_count=self.row_count, column_count=self.column_count)

    for i in range(self.row_count):
      for j in range(self.column_count):
        added_matrix[i, j] = self[i, j] + other[i, j]

    return added_matrix

  def __iadd__(self: Matrix, other: Matrix):
    if not isinstance(self, Matrix) or not isinstance(other, Matrix):
      raise ValueError("elements must be matrices")

    if self.row_count != other.row_count or self.column_count != other.column_count:
       raise ValueError("Matrices must be of the same dimensions!")

    for i in range(self.row_count):
      for j in range(self.column_count):
        self[i, j] = self[i, j] + other[i, j]

    return self

  def __sub__(self: Matrix, other: Matrix):
    if not isinstance(self, Matrix) or not isinstance(other, Matrix):
       raise ValueError("elements must be matrices")

    if self.row_count != other.row_count or self.column_count != other.column_count:
       raise ValueError("Matrices must be of the same dimensions!")

    added_matrix = Matrix(row_count=self.row_count, column_count=self.column_count)

    for i in range(self.row_count):
      for j in range(self.column_count):
        added_matrix[i, j] = self[i, j] - other[i, j]

    return added_matrix

  def __isub__(self: Matrix, other: Matrix):
    if not isinstance(self, Matrix) or not isinstance(other, Matrix):
       raise ValueError("elements must be matrices")

    if self.row_count != other.row_count or self.column_count != other.column_count:
       raise ValueError("Matrices must be of the same dimensions!")

    for i in range(self.row_count):
      for j in range(self.column_count):
        self[i, j] = self[i, j] - other[i, j]

    return self

  def __mul__(self: Matrix, other: Matrix | int | float):
    if isinstance(self, Matrix) and (isinstance(other, int) or isinstance(other, float)):
      mul_matrix = Matrix(row_count=self.row_count, column_count=self.column_count)

      for i in range(self.row_count):
          for j in range(self.column_count):
              mul_matrix[i, j] = self[i, j] * other

      return mul_matrix


    if not isinstance(self, Matrix) or not isinstance(other, Matrix):
      raise ValueError("elements must be matrices")

    if self.column_count != other.row_count:
      raise ValueError("Matrices must have dimensions ixj jxk")

    mul_matrix = Matrix(row_count=self.row_count, column_count=other.column_count)

    for i in range(self.row_count):
      for k in range(other.column_count):
        mul_matrix[i, k] = 0
        for j in range(self.column_count):
          mul_matrix[i,k] = mul_matrix[i,k] + self[i,j] * other[j,k]

    return mul_matrix

  def __rmul__(self: Matrix, other: int | float | Matrix) -> Matrix:
    return self.__mul__(other)

  # def __eq__(self: Matrix, other: Matrix):
  #   if not isinstance(self, Matrix) or not isinstance(other, Matrix):
  #      raise ValueError("elements must be matrices")

  #   if self.row_count != other.row_count:
  #     return False

  #   if self.column_count != other.column_count:
  #     return False

  #   for i in range(self.row_count):
  #     for j in range(self.column_count):
  #       if self[i, j] != other[i, j]:
  #         return False

  #   return True

  def __invert__(self):
    transponsed = Matrix(row_count=self.column_count, column_count=self.row_count)

    for i in range(self.row_count):
      for j in range(self.column_count):
        transponsed[j, i] = self[i, j]

    return transponsed

  def __neg__(self):
    return -1*self

  def __str__(self):
    output = ""
    for i in range(self.row_count):
      for j in range(self.column_count):
        output += str(self[i, j])
        if j < self.column_count - 1:
          output += " "
      output += "\n"

    return output

  #TODO
  def _init_from_file(self):
    with open(self.file, "r") as file:
      lines = file.readlines()

    self.row_count = len(lines)
    self.column_count = len(lines[0].strip().split(" "))
    self._init_empty()

    for i, line in enumerate(lines):
      row = line.strip().split(" ")

      for j, el in enumerate(row):
        fraction = el.split("/")
        if len(fraction) == 2:
          a, b = fraction
          self[i, j] = float(a) / float(b)

          continue

        self[i, j] = float(el)

  def _init_empty(self):
    self.elements = []
    for _ in range(self.row_count):
      row = []
      for _ in range(self.column_count):
          row.append(0.0)
      self.elements.append(row)

  def _init_from_elements(self, elements):
    self._init_empty()
    for i in range(self.row_count):
      for j in range(self.column_count):
        self[i, j] = elements[i][j]

  def _is_square(self: Matrix):
    return self.row_count == self.column_count

  def _extract_column(self: Matrix, j: int) -> Matrix:
    out = Matrix(row_count=self.row_count, column_count=1)
    for i in range(self.row_count):
      out[i] = self[i, j]

    return out

  def swap_rows(self: Matrix, x: int, y: int):
    tmp = self.elements[x]
    self.elements[x] = self.elements[y]
    self.elements[y] = tmp

  def forward_substitution(self: Matrix, b: Matrix):
    if not self._is_square():
      raise ValueError("Must be square matrix")

    if self.row_count != b.row_count:
      raise ValueError("Unsupported operation")

    if b.column_count != 1:
      raise ValueError("Unsupported operation")

    y = copy.deepcopy(b)
    for i in range(self.row_count - 1):
      for j in range(i + 1, self.column_count):
        y[j, 0] -= self.A[j,i] * y[i, 0];

    return y

  def back_substitution(self: Matrix, b: Matrix):
    if not self._is_square():
      raise ValueError("Must be square matrix")

    if self.row_count != b.row_count:
      raise ValueError("Unsupported operation")

    if b.column_count != 1:
      raise ValueError("Unsupported operation")

    return_vector = copy.deepcopy(b)

    for i in range(self.row_count - 1, -1, -1):
      if abs(self.A[i, i]) < EPSILON:
        raise ValueError("input is a singular matrix")

      return_vector[i] /= self.A[i,i]
      for j in range(i):
        return_vector[j] -= self.A[j, i] * return_vector[i]

    return return_vector

  def lu_decomposition(self: Matrix):
    if not self._is_square():
      raise ValueError("input needs to be a square matrix")

    self.A = copy.deepcopy(self)

    for i in range(0, self.row_count):
      for j in range(i + 1, self.column_count):
        if abs(self.A[i, i]) < EPSILON:
          raise ValueError("matrix is singular")

        self.A[j, i] /= self.A[i, i]

        for k in range(i + 1, self.row_count):
          self.A[j, k] -= self.A[j, i] * self.A[i, k]

  def lup_decomposition(self: Matrix):
    if not self._is_square():
      raise ValueError("input needs to be a square matrix")

    self.A = copy.deepcopy(self)
    self.P = Matrix(row_count=self.row_count, column_count=self.column_count)

    for i in range(self.row_count):
      self.P[i, i] = 1

    self.row_swap_count = 0

    for i in range(0, self.row_count):
      pivot_value = 0
      pivot = i

      for j in range(i, self.row_count):
        if abs(self.A[j, i]) > pivot_value:
          pivot_value = abs(self.A[j, i])
          pivot = j

      if pivot != i:
        self.A.swap_rows(pivot, i)
        self.P.swap_rows(pivot, i)
        self.row_swap_count += 1


      for j in range(i + 1, self.column_count):
        if abs(self.A[i, i]) < EPSILON:
          raise ValueError("matrix is singular")

        self.A[j, i] /= self.A[i, i]

        for k in range(i + 1, self.row_count):
          self.A[j, k] -= self.A[j, i] * self.A[i, k]

  def inverse(self: Matrix):
    try:
      self.lup_decomposition()

      inversed = Matrix(row_count=self.row_count, column_count=self.column_count)
      for i in range(self.row_count):
        e = self.P._extract_column(i)
        y = self.forward_substitution(e)
        x = self.back_substitution(y)

        for j in range(x.row_count):
          inversed[j, i] = x[j]
    except ValueError:
      return "Fail"

    return inversed

  def determinant(self: Matrix):
    try:
      self.lup_decomposition()

      det_P = (-1)**self.row_swap_count
      for i in range(self.A.row_count):
        det_P *= self.A[i, i]

      return det_P

    except ValueError:
      return "Fail"

  def lu_solve(self: Matrix, b: Matrix):
    try:
      self.lu_decomposition()
      y = self.forward_substitution(b)
      x = self.back_substitution(y)

    except ValueError:
      return "Fail"

    return x

  def lup_solve(self: Matrix, b: Matrix):
      try:
        self.lup_decomposition()
        y = self.forward_substitution(self.P * b)
        x = self.back_substitution(y)

      except ValueError:
        return "Fail"

      return x
