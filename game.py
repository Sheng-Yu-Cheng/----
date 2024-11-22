from block import *
from player import *

# game status:
# wait commnd
# do animation


class GameStatus:
    WAIT_PLAYER_COMMAND = 0
    DOING_ANIMATION = 1

class Game:
    def __init__(self, blocks, players):
        self.block_amount = len(blocks)
        self.blocks = blocks
        self.player_amount = len(players)
        self.players = players
        self.status = GameStatus.WAIT_PLAYER_COMMAND
    def rollDice(self, ):
        
