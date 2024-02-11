import logging
from random import randint
from time import sleep, time
from dataclasses import dataclass, field
from enum import IntEnum, auto
from typing import Dict, Optional
from mpi4py import MPI


class Tags(IntEnum):
    RIGHT_FORK_REQUEST = auto()
    LEFT_FORK_REQUEST = auto()
    RIGHT_FORK_SEND = auto()
    LEFT_FORK_SEND = auto()

@dataclass
class Fork:
  clean: bool = False

@dataclass
class Requests:
  right_fork_request: bool
  left_fork_request: bool


@dataclass
class Philosopher:
  comm: MPI.Intracomm
  rank: int
  size: int
  name: str

  left_fork: Optional[Fork] = field(init=False)
  right_fork: Optional[Fork] = field(init=False)

  left_neighbour_rank: int = field(init=False)
  right_neighbour_rank: int = field(init=False)

  left_fork_request_sent: bool = False
  right_fork_request_sent: bool = False

  left_fork_request_received: bool = False
  right_fork_request_received: bool = False


  def neighbours_init(self):
    self.left_neighbour_rank = self.size - 1 if self.rank == 0 else self.rank - 1
    self.right_neighbour_rank = 0 if self.rank == self.size - 1 else self.rank + 1


  def forks_init(self):
    if self.rank == 0:
      self.left_fork, self.right_fork = Fork(), Fork()
    elif self.rank == self.size - 1:
      self.left_fork, self.right_fork = None, None
    else:
      self.left_fork, self.right_fork = None, Fork()


  def __post_init__(self):
    self.neighbours_init()
    self.forks_init()

    logging.debug(f"{self.indent()}Bok, ja sam {self.name}")


  def has_both_forks(self) -> bool:
    return self.left_fork is not None and self.right_fork is not None


  def think(self):
    sleep_time = randint(1,3)
    duration = time() + sleep_time
    logging.debug(f"{self.indent()}Mislim {sleep_time}s.")

    while time() < duration:
      self.process_requests()


  def eat(self):
    eat_time = randint(1, 3)
    sleep(eat_time)

    logging.debug(f"{self.indent()}Jedem {eat_time}s.")

    self.right_fork.clean = False
    self.left_fork.clean = False


  def process_requests(self):
      self.process_fork_request("right")
      self.process_fork_request("left")


  def process_fork_request(self, fork_side: str):
    source = getattr(self, f"{fork_side}_neighbour_rank")
    source_request = "left" if fork_side == "right" else "right"
    tag = Tags.LEFT_FORK_REQUEST if source_request == "left" else Tags.RIGHT_FORK_REQUEST

    if self.comm.Iprobe(source=source, tag=tag):
      self.comm.recv(source=source, tag=tag)
      logging.debug(f"{self.indent()}Stize zahtjev za moju {fork_side} vilicu")
      # log Zahtjev za mojoj vilicom, ako je fork side RIGHT onda za mojom LIJEVOM od LIJEVOG susjeda (on REQUESTA DESNU)

      fork_attr: Fork = getattr(self, f"{fork_side}_fork")
      if fork_attr is not None and not fork_attr.clean:
        self.send_fork(fork_side)
      else:
        logging.debug(f"{self.indent()}Biljezim zahtjev za moju {fork_side} vilicu")
        setattr(self, f"{fork_side}_fork_request_received", True)


  def send_fork(self, fork_side):
    fork: Fork = getattr(self, f"{fork_side}_fork")
    fork.clean = True
    tag = Tags.LEFT_FORK_SEND if fork_side == "left" else Tags.RIGHT_FORK_SEND

    self.comm.send(fork, dest=getattr(self, f"{fork_side}_neighbour_rank"), tag=tag)
    logging.debug(f"{self.indent()}Saljem svoju {fork_side} vilicu")

    setattr(self, f"{fork_side}_fork", None)


  def process_responses(self):
    self.process_fork_response("right")
    self.process_fork_response("left")


  def process_fork_response(self, fork_side):
    source = getattr(self, f"{fork_side}_neighbour_rank")
    source_response = "left" if fork_side == "right" else "right"
    tag = Tags.LEFT_FORK_SEND if source_response == "left" else Tags.RIGHT_FORK_SEND

    if self.comm.Iprobe(source=source, tag=tag):
      fork = self.comm.recv(None, source=source, tag=tag)
      setattr(self, f"{fork_side}_fork", fork)
      logging.debug(f"{self.indent()}Dobivam {fork_side} vilicu")
      setattr(self, f"{fork_side}_fork_request_sent", False)


  def process_other_requests(self):
    if self.left_fork_request_received:
      self.send_fork('left')
      self.left_fork_request_received = False
    elif self.right_fork_request_received:
      self.send_fork('right')
      self.right_fork_request_received = False


  def send_fork_request(self, fork_side: str):
    if getattr(self, f"{fork_side}_fork") is not None or getattr(self, f"{fork_side}_fork_request_sent"):
      return

    tag = Tags.LEFT_FORK_REQUEST if fork_side == "left" else Tags.RIGHT_FORK_REQUEST
    self.comm.send(None, dest=getattr(self, f"{fork_side}_neighbour_rank"), tag=tag)
    logging.debug(f"{self.indent()}Trazim {fork_side} vilicu")
    setattr(self, f"{fork_side}_fork_request_sent", True)


  def indent(self):
    return f"{self.name}: " + "    " * self.rank

def main():
  logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] %(message)s",
    datefmt="%H:%M:%S",
  )

  comm = MPI.COMM_WORLD
  rank = comm.Get_rank()
  size = comm.Get_size()

  philosopher = Philosopher(comm, rank, size, f"Phil {rank}")

  while True:
    philosopher.think()

    while not philosopher.has_both_forks():
      # salji zahtjev za desnom vilicom
      philosopher.send_fork_request("left")

      while philosopher.left_fork is None:
        philosopher.process_responses()
        philosopher.process_requests()

      # salji zahtjev za lijevom vilicom
      philosopher.send_fork_request("right")

      while philosopher.right_fork is None:
        philosopher.process_responses()
        philosopher.process_requests()

    philosopher.eat()
    philosopher.process_other_requests()


if __name__ == "__main__":
  try:
      main()
  except KeyboardInterrupt:
      pass
