import pygame
from typing import List

class PlayerStatus:
    NOT_IN_JAIL = 0b0
    IN_JAIL = 0b1

class PlayerToken:
    def __init__(self, image: pygame.Surface):
        self.image: pygame.Surface = image
        self.rect: pygame.Rect = image.get_rect()

class Player:
    def __init__(self, name, index, token: PlayerToken, position = 0, balance = 0, status = PlayerStatus.NOT_IN_JAIL):
        self.name = name
        self.index = index
        self.position = position
        self.status = status
        self.balance = balance
        #
        self.stop_round = 0
        #
        self.token = token
        self.token_position = position
    def renderToScreen(self, screen: pygame.Surface):
        screen.blit(self.token.image, self.token.rect)


