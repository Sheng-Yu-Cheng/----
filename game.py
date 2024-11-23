from block import *
from player import *
from game_board import *
from action_menu import *
from typing import List, Union

class GameStatus:
    GENERAL = 0


class Game:
    def __init__(self, screen_size, board: GameBoard, players: List[Player], status = GameStatus.GENERAL):
        self.screen_width, self.screen_height = screen_size
        self.board = board
        self.block_amount = len(self.board.blocks)
        self.player_amount = len(players)
        self.players = players
        self.action_menu = ActionMenuWindow(screen_size)
        self.status = status
    def playerGoAhead(self, player_index, steps):
        self.players[player_index].position += steps
        self.players[player_index].position %= self.block_amount
        return self.blocks[self.players[player_index].position]
    def renderToScreen(self, screen: pygame.Surface):
        self.action_menu.renderToScreen(screen)
        if self.status == GameStatus.GENERAL:
            self.board.renderToScreen(screen, [False for _ in range(self.block_amount)])
    

