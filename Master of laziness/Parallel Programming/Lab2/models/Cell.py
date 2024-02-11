from models.Player import Player
from consts.board import EMPTY_CHAR

class Cell:
  def __init__(self) -> None:
    self.player = None

  def value(self):
    return EMPTY_CHAR if self.player is None else self.player.char

  def set(self, player: Player):
    self.player = player
