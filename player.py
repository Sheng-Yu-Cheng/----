class PlayerStatus:
    NOT_IN_JAIL = 0b0
    IN_JAIL = 0b1

class Player:
    def __init__(self, name, index, position = 0, properties = [], status = PlayerStatus.NOT_IN_JAIL):
        self.name = name
        self.index = index
        self.position = position
        self.status = status
        self.properties = properties
    def goto(self, position):
        self.position = position
