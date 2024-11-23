from block import *
from typing import Union, List
import pygame


s
class ClassicBoard:
    def __init__(self, blocks: List[Block], blocks_image):
        self.block_images = []
        self.block_images = []
        self.blocks = blocks
        self.block_amount = len(self.blocks)
        self.width, self.height = 60, 80
        x = [20] + [100 + 60 * i for i in range(10)] + [620 for i in range(10)] + [560 - i * 60 for i in range(10)] + [20 for i in range(9)]
        y = [20] + [20 for i in range(10)] + [100 + i * 60 for i in range(10)] + [620 for i in range(10)] +  + [560 - i * 60 for i in range(10)]
        print(x, y)
        for i, block in enumerate(self.blocks):
            if block.type in BlockType.CORNER:
                image = pygame.transform.rotate(pygame.image.load("Assets/Classic Board/Corner.png"), rot)
                image_rect = image.get_rect()
                image_rect.topleft = (x[i], y[i])
        
classic = ClassicBoard()