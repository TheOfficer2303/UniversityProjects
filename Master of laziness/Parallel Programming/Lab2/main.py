import itertools
import logging
import math
from copy import deepcopy
from functools import reduce

from mpi4py import MPI

from models.Board import Board
from models.Player import Player, PlayerType

from consts.depth import TASKS_GENERATION_DEPTH
from consts.board import BOARD_LENGTH, USER_CHAR, CPU_CHAR
from consts.comm import MASTER_PROCESS, Tags

COMM = MPI.COMM_WORLD
SIZE = COMM.Get_size()
RANK = COMM.Get_rank()
name = MPI.Get_processor_name()

def stop_workers():
  for i in range(1, SIZE):
    COMM.send(None, i, Tags.NO_MORE_TASKS)

def get_tasks():
  column_indexes = []
  for _ in range(TASKS_GENERATION_DEPTH):
    column_indexes.append(list(range(0, BOARD_LENGTH)))

  moves = []
  for combination in itertools.product(*column_indexes):
    moves.append(combination)

  return moves

def choose_best_move(board:Board, results: dict):
  best_results = []
  move = None

  for column, values in results.items():
    if any(value == -1 for value in values):
      best_results.append(PlayerType.USER_PLAYER.value)
      print(f"{column} -1")
    elif all(value == 1 for value in values):
        best_results.append(PlayerType.CPU_PLAYER.value)
        print(f"{column} 1")
    else:
        average_value = sum(values) / len(values)
        best_results.append(average_value)
        print(f"{column}: {average_value}")

  temp_results = best_results.copy()
  while move is None:
    max_index = max(range(len(temp_results)), key=temp_results.__getitem__)
    temp = max_index

    temp_results[temp] = -math.inf
    if temp in board.get_valid_move_indexes():
      move = temp
      break

  return move

def make_cpu_move(board: Board):
  tasks_to_send = get_tasks()
  received_results = 0
  source = 0
  results = {i: list() for i in range(0, BOARD_LENGTH)}
  tasks_sent = len(tasks_to_send)

  while received_results != tasks_sent:
    if source >= SIZE or source == 0:
      source = MASTER_PROCESS + 1

    status = MPI.Status()
    message = COMM.recv(source=source, status=status)

    if status.tag == Tags.GIVE_TASK:
      if len(tasks_to_send) > 0:
        send_load = (tasks_to_send.pop(), deepcopy(board))
        COMM.send(send_load, source, Tags.TASK_SEND)
      else:
        COMM.send("Wait", source, Tags.WAIT)

    elif status.tag == Tags.RESULT_SEND:
      received_results += 1
      result, column = message
      results[column].append(result)

    source += 1

  move = choose_best_move(board, results)
  board.make_move(move)

def worker_process():
  while True:
    COMM.send('Give Task', 0, Tags.GIVE_TASK)

    status = MPI.Status()
    message = COMM.recv(source=MPI.ANY_SOURCE, status=status)

    if status.tag == Tags.WAIT:
      continue
    if status.tag == Tags.NO_MORE_TASKS:
      break
    elif status.tag == Tags.TASK_SEND:
      moves, board = message
      winner = board.make_moves(moves)

      if winner:
        result = winner.value
      else:
        result = board.evaluate(depth=1)

      COMM.send((result, moves[0]), 0, Tags.RESULT_SEND)

def get_user_input():
  user_column = int(input('Input column number: '))
  while True:
    if user_column > 0 and user_column <= BOARD_LENGTH:
      break

    user_column = int(input('Input column number: '))

  return user_column - 1


def master_process():
  player_1 = Player("Player 1 (User)", USER_CHAR, -1, PlayerType.USER_PLAYER)
  player_2 = Player("Player 2 (CPU)", CPU_CHAR, 1, PlayerType.CPU_PLAYER)
  board = Board(player_1, player_2)

  game_on = True

  while game_on:
    user_column = get_user_input()

    board.make_move(user_column)
    board.print()

    if board.has_winner():
      stop_workers()
      game_on = False
      continue

    start = MPI.Wtime()
    make_cpu_move(board)
    end = MPI.Wtime()
    print(f"Time elapsed: {end - start}")
    board.print()

    if board.has_winner():
      stop_workers()
      game_on = False
      continue

def main():
  if RANK == 0:
      master_process()
  else:
      worker_process()

if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    pass
