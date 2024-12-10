from font_machine import *
import pygame
import time
import random
from typing import List

random.seed(time.time())

class Dice:
    def __init__(self):
        self.dice_images = [pygame.image.load(f"Assets/Dice/dice{i}.png") for i in range(1, 7)]
        self.dice_rect = (self.dice_images[0].get_rect(), self.dice_images[0].get_rect())
        self.dice_rect[0].topleft = (110, 110)
        self.dice_rect[1].topleft = (170, 110)
        self.dice_result = (6, 6)
        #
        self.roll_dice_button = COMIC_SANS18.render("-ROLL DICE-", 1, "#FFFFFF", "#000000")
        self.roll_dice_button_rect = self.roll_dice_button.get_rect()
        self.roll_dice_button_rect.topleft = (110, 170)
    def rollDice(self):
        self.dice_result = (random.randint(1, 6), random.randint(1, 6))
    def renderToScreen(self, screen: pygame.Surface):
        screen.blit(self.dice_images[self.dice_result[0] - 1], self.dice_rect[0])
        screen.blit(self.dice_images[self.dice_result[1] - 1], self.dice_rect[1])
        screen.blit(self.roll_dice_button, self.roll_dice_button_rect)
