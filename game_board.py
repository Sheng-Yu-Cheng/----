from block import *
from constant import *
from typing import Union, List, Tuple
import pygame

class GameBoard:
    def __init__(self):
        self.blocks : List[BLOCK] = []
        self.masks : List[Tuple[pygame.Surface, pygame.Rect]] = []
    def addBlock(self, block: BLOCK):
        self.blocks.append(block)
        mask = pygame.Surface((block.rect.width, block.rect.height), pygame.SRCALPHA)
        mask.fill((0, 0, 0, 100))
        mask_rect = mask.get_rect()
        mask_rect.topleft = block.rect.topleft
        self.masks.append((mask, mask_rect))
    def renderToScreen(self, screen: pygame.Surface, mask: List[bool]):
        for i, block in enumerate(self.blocks):
            screen.blit(block.image, block.rect)
            if mask[i]:
                screen.blit(self.masks[i][0], self.masks[i][1])

def generateClassicGameBoard() -> GameBoard:
    board = GameBoard()
    #
    pall_mall_image = pygame.transform.rotate(pygame.image.load("Assets/Classic Board/red.png"), 270)
    pall_mall = StreetBlock(pall_mall_image, "Pall Mall", 11, 140, 70, [10, 20, 30, 40, 50], [10, 15, 20, 25, 30, 35], "red", 0)
    pall_mall.rect.topleft = (20, 580)
    board.addBlock(pall_mall)
    #
    return board