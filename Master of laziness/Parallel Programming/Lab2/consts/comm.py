from enum import Enum, IntEnum, auto

class Tags(IntEnum):
  GIVE_TASK = auto()
  TASK_SEND = auto()
  RESULT_SEND = auto()
  NO_MORE_TASKS = auto()
  WAIT = auto()

MASTER_PROCESS = 0
