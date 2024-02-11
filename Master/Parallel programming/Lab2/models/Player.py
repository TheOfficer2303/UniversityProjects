from dataclasses import dataclass
from enum import Enum

class PlayerType(Enum):
  USER_PLAYER = -1
  CPU_PLAYER = 1

@dataclass
class Player:
  label: str
  char: str
  value: int
  player_type: PlayerType
