from block import *
from player import *
from typing import List, Union

class Game:
    def __init__(self, blocks: List[Union[StreetBlock, RailroadBlock, UtilityBlock]], players: List[Player]):
        self.block_amount = len(blocks)
        self.blocks = blocks
        self.player_amount = len(players)
        self.players = players
    def playerGoAhead(self, player_index, steps):
        self.players[player_index].position += steps
        self.players[player_index].position %= self.block_amount
        return self.blocks[self.players[player_index].position]
    

