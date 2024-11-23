from block import *
from constant import *
from typing import Union, List
import pygame


class GameBoard:
    def __init__(self):
        self.blocks : List[BLOCK] = []
    def addBlock(self, block: BLOCK):
        self.blocks.append(block)
    def renderToScreen(self, screen: pygame.Surface):
        for block in self.blocks:
            screen.blit(block.image, block.rect)

def generateClassicGameBoard() -> GameBoard:
    board = GameBoard()
    #
    start_image = pygame.image.load("Assets/Classic Board/corner.png", )

    start = StartBlock()
    board.addBlock(start)
    return board