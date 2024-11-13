from block import *
from player import *

class Game:
    def __init__(self, blocks, players):
        self.block_amount = len(blocks)
        self.blocks = blocks
        self.player_amount = len(players)
        self.players = players
    def movePlayerTo(self, index, position):
        self.players[index] 
