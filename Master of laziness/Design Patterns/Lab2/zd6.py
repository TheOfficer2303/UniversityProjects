from __future__ import annotations

from abc import ABC, abstractmethod
import ast
from dataclasses import dataclass, field
import re
from typing import List


@dataclass
class Observer(ABC):
  @abstractmethod
  def update(self):
    pass


@dataclass
class Subject(ABC):
  observers: List[Observer] = field(default_factory=Observer, init=False)

  @abstractmethod
  def attach(self, observer):
    pass

  @abstractmethod
  def dettach(self, observer):
    pass

  @abstractmethod
  def notify(self):
    pass


@dataclass
class Cell(Subject, Observer):
  name: str
  exp: str
  sheet: Sheet
  value: int = field(init=False)

  observers: List[Observer] = field(default_factory=list, init=False)

  def set(self, exp):
    self.exp = exp
    self.evaluate()

  def evaluate(self):
    self.value = self.sheet.evaluate(self)
    self.notify()

  def notify(self):
    for o in self.observers:
      o.update()

  def attach(self, observer):
    self.observers.append(observer)

  def dettach(self, observer):
    self.observers.remove(observer)

  def update(self):
    self.evaluate()

  def __hash__(self) -> int:
    return self.name.__hash__()


@dataclass
class Sheet:
  n_rows: int
  n_columns: int

  cells: List[List[Cell]] = field(default_factory=list)

  def __post_init__(self):
    first_row = 1
    first_column = "A"

    self.cells = [["" for j in range(self.n_columns)] for i in range(self.n_rows)]

    for i in range(self.n_rows):
      for j in range(self.n_columns):
        cell_column_name = chr(ord(first_column) + j)
        cell_row_name = first_row + i
        cell_name = f"{cell_column_name}{cell_row_name}"
        self.cells[i][j] = Cell(cell_name, "-", self)

  def cell(self, name: str):
    column = ord(list(name)[0]) - 65
    row = int(list(name)[1]) - 1

    return self.cells[row][column]

  def getrefs(self, cell: Cell):
    if not re.search('[A-Z]', cell.exp):
      return []
    cell_refs = cell.exp.split("+")
    cells = [self.cell(cf) for cf in cell_refs]

    return cells

  def set(self, ref: str, content: str):
    cell = self.cell(ref)

    #check cycles
    if re.search('[A-Z]', content):
      has_cycle = self.check_for_cycles(cell, content)
      if has_cycle:
        raise ValueError("Cycle detected!")

    #update observer cells
    self.update_observers(cell, content)

    cell.set(content)


  def update_observers(self, cell: Cell, content: str):
    current_referenced_cells = set()
    current_referenced_cells = set(self.getrefs(cell))

    new_referenced_cells = set()
    if re.search('[A-Z]', content):
      new_referenced_cells_list = [self.cell(name) for name in content.split("+")]
      new_referenced_cells = set(new_referenced_cells_list)

    to_detach = current_referenced_cells.difference(new_referenced_cells)
    to_attach = new_referenced_cells.difference(current_referenced_cells)

    for rc in list(to_detach):
      rc.dettach(cell)
      print(f"{cell.name} is no longer observing {rc.name}")

    for rc in list(to_attach):
      rc.attach(cell)
      print(f"{cell.name} is now observing {rc.name}")

  def check_for_cycles(self, cell: Cell, content: str):
    start_referenced_cells = content.split("+")
    visited = set()
    new_referenced_cells = []
    is_error = False

    referenced_cells = start_referenced_cells
    while True:
      for rc in referenced_cells:
        visited.add(self.cell(rc).name)
        c = self.cell(rc)
        new_cells = self.getrefs(c)
        if len(new_cells) > 0:
          new_referenced_cells.extend(cl.name for cl in self.getrefs(c))

      referenced_cells = new_referenced_cells
      new_referenced_cells = []
      if cell.name in visited:
        is_error = True
        break

      if len(referenced_cells) == 0:
        break

    return is_error

  def evaluate(self, cell: Cell):
    def _eval(node: ast.expr) -> int:
      if isinstance(node, ast.Num):
          return node.n
      elif isinstance(node, ast.Name):
          return self.cell(node.id).value
      elif isinstance(node, ast.BinOp):
          return _eval(node.left) + _eval(node.right)
      else:
        raise Exception(f"Unsupported type {node}")

    ast_node = ast.parse(cell.exp, mode="eval")
    return _eval(ast_node.body)

  def print(self):
    for i in range(self.n_rows):
      for j in range(self.n_columns):
        if hasattr(self.cells[i][j], "value"):
          output = self.cells[i][j].value
        else:
          output = "-"
        print(output, end="    ")
      print()

def main():
  s=Sheet(5,5)
  print()

  s.set('A1','2')
  s.set('A2','5')
  s.set('A3','A1+A2')
  s.print()
  print()

  s.set('A1','4')
  s.set('A4','A1+A3')
  s.print()
  print()

  s.set('B1', 'A3')
  s.print()
  print()

  s.set('A1', '7')
  s.print()
  print()

  try:
    s.set('A1','A3')
  except ValueError as e:
    print("Caught exception:",e)
  s.print()
  print()

if __name__=="__main__":
  main()
