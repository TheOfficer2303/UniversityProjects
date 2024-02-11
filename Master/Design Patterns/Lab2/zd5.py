from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from time import sleep
from datetime import datetime
from typing import List
from statistics import median

@dataclass
class Observer(ABC):
  @abstractmethod
  def update(self, state):
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
class NumberSource(ABC):
  has_more: bool = field(init=False)

  @abstractmethod
  def get_number(self):
    pass


@dataclass
class KeyboardSource(NumberSource):
  has_more = True

  def get_number(self):
    while True:
      try:
        number = int(input("Input a number: "))
      except ValueError:
        print("Wrong input!")
        continue

      if number == -1:
        self.has_more = False

      return number


@dataclass
class FileSource(NumberSource):
  path: str
  numbers: List[int] = field(default_factory=list, init=False)

  has_more = True

  def __post_init__(self):
    with open(self.path) as file:
      lines = file.readlines()

      for line in lines:
        try:
          number = int(line)
        except ValueError:
          print("Wrong input")
          continue

        self.numbers.append(number)


  def get_number(self):
    length = len(self.numbers)
    if length != 0:
      return self.numbers.pop(length - 1)
    else:
      self.has_more = False


@dataclass
class FileLoggerObserver(Observer):
  path: str

  def update(self, state):
    with open(self.path, "a") as file:
      file.write(f"{datetime.now()} {state}\n")



@dataclass
class SumOfElementsObserver(Observer):
  def update(self, state: List[int]):
    print(f"Sum of numbers: {sum(state)}")


@dataclass
class AverageOfElementsObserver(Observer):
  def update(self, state: List[int]):
    print(f"Average of numbers: {round(sum(state) / len(state), 2)}")


@dataclass
class MedianOfElementsObserver(Observer):
  def update(self, state: List[int]):
    print(f"Median of numbers: {round(median(state), 2)}")


@dataclass
class NumberSequence(Subject):
  numbers: List[int] = field(default_factory=list, init=False)
  numberSource: NumberSource
  observers: List[Observer] = field(default_factory=list, init=False)

  def start(self):
    while True:
      number: int = self.numberSource.get_number()

      if not self.numberSource.has_more:
        break

      self.numbers.append(number)
      self.notify()

      sleep(1)

  def attach(self, observer):
    self.observers.append(observer)

  def dettach(self, observer):
    self.observers.remove(observer)

  def notify(self):
    for o in self.observers:
      o.update(self.numbers)


def main():
  numberSource = KeyboardSource()
  numberSequence = NumberSequence(numberSource)

  ob1 = SumOfElementsObserver()
  ob2 = AverageOfElementsObserver()
  ob3 = MedianOfElementsObserver()
  ob4 = FileLoggerObserver("output.txt")
  numberSequence.attach(ob1)
  numberSequence.attach(ob2)
  numberSequence.attach(ob3)
  numberSequence.attach(ob4)

  numberSequence.start()
  print(numberSequence.numbers)


if __name__ == "__main__":
  main()
