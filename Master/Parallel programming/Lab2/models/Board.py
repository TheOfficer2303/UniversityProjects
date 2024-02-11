from copy import deepcopy
from consts.board import BOARD_HEIGHT, BOARD_LENGTH, EMPTY_CHAR
from consts.depth import RECURSION_DEPTH

from models.Cell import Cell
from models.Player import Player


class Board:
  def __init__(self, player_1: Player, player_2: Player) -> None:
    self.board = [[Cell() for i in range(BOARD_LENGTH)] for j in range(BOARD_HEIGHT)]
    self.move_stack = []
    self.players = {
      "user": player_1,
      "cpu": player_2
    }
    self.player_on_move = player_1
    self.last_player = None
    self.print()

  def make_move(self, column: int):
    row = self.get_free_row_index(column)

    if row is None:
      return False


    self.board[row][column].player = self.player_on_move
    self.move_stack.append((row, column))

    self.last_player = deepcopy(self.player_on_move)
    self.player_on_move = self.players["cpu"] if self.player_on_move == self.players["user"] else self.players["user"]


  def get_valid_move_indexes(self):
    return [index + 1 for index in range(BOARD_LENGTH) if self.board[BOARD_HEIGHT - 1][index].value() == EMPTY_CHAR]


  def get_free_row_index(self, column: int):
    for i in range(0, BOARD_HEIGHT):
      if self.board[i][column].value() == EMPTY_CHAR:
        return i

    return None


  def undo(self):
    if len(self.move_stack):
      i, j = self.move_stack.pop()
      self.board[i][j].player = None


  def make_moves(self, moves: tuple):
    for move in moves:
      if move in self.get_valid_move_indexes():
        self.make_move(move)

        if self.has_winner():
          winner = self.last_player
          return winner

  def has_winner(self):
    for i in range(BOARD_HEIGHT):
      for j in range(BOARD_LENGTH):
        cell_value = self.board[i][j].value()

        if cell_value == EMPTY_CHAR:
          continue

        if j < BOARD_LENGTH - 3:
          if cell_value == self.board[i][j + 1].value() == self.board[i][j + 2].value() == self.board[i][j + 3].value():
              return True

        if i < BOARD_HEIGHT - 3:
          if cell_value == self.board[i + 1][j].value() == self.board[i + 2][j].value() == self.board[i + 3][j].value():
              return True

        if i < BOARD_HEIGHT - 3 and j < BOARD_LENGTH - 3:
          if cell_value == self.board[i + 1][j + 1].value() == self.board[i + 2][j + 2].value() == self.board[i + 3][j + 3].value():
              return True

        if i >= 3 and j < BOARD_LENGTH - 3:
          if cell_value == self.board[i - 1][j + 1].value() == self.board[i - 2][j + 2].value() == self.board[i - 3][j + 3].value():
              return True

    return False


  def print(self):
    flipped_array = self.board[::-1]
    for i in range(BOARD_HEIGHT):
      for j in range(BOARD_LENGTH):
        print(flipped_array[i][j].value(), end=" ")
      print()


  def evaluate(self, depth: int):
    if self.has_winner():
      return self.last_player.value

    if depth == RECURSION_DEPTH:
      return 0

    valid_moves = self.get_valid_move_indexes()
    child_values_sum = 0
    player_always_win, cpu_always_win = True, True

    for column in range(0, BOARD_LENGTH):
      if column not in valid_moves:
        continue

      self.make_move(column)
      result = self.evaluate(depth+1)
      self.undo()

      if result != self.players["user"].value:
        player_always_win = False

      if result != self.players["cpu"].value:
        cpu_always_win = False

      if result == self.players["cpu"].value and self.player_on_move == self.players["cpu"]:
        return self.players["cpu"].value

      if result == self.players["user"].value and self.player_on_move == self.players["user"]:
        return self.players["user"].value

      child_values_sum += result

    if cpu_always_win:
      return self.players["cpu"].value
    elif player_always_win:
      return self.players["user"].value

    return child_values_sum / len(valid_moves)
