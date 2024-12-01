from typing import List

class PlayerStatus:
    NOT_IN_JAIL = 0b0
    IN_JAIL = 0b1

class Player:
    def __init__(self, name, index, position = 0, balance = 0, status = PlayerStatus.NOT_IN_JAIL):
        self.name = name
        self.index = index
        self.position = position
        self.status = status
        self.balance = balance


