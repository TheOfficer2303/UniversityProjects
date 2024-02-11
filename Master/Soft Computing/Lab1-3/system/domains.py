from domain.domain import SimpleDomain

class Domains():
  ANGLE = SimpleDomain(-90, 90 + 1)
  DISTANCE = SimpleDomain(0, 1300 + 1)

  SPEED = SimpleDomain(0, 100 + 1)
  ACCELERATION = SimpleDomain(-50, 50 + 1)

  ORIENTATION = SimpleDomain(0, 1 + 1)
