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
    pall_mall_image = pygame.transform.rotate(pygame.image.load("Assets/Classic Board/red.png"), 270)
    pall_mall = StreetBlock(pall_mall_image, "Pall Mall", 11, 140, 70, [10, 20, 30, 40, 50], [10, 15, 20, 25, 30, 35], "red", 0)
    pall_mall.rect.topleft = (20, 580)
    board.addBlock(pall_mall)
    #
    return board