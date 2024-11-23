from block import *
from player import *
from font_machine import *
from utilities import *
from typing import List, Tuple, Union
import pygame

class ActionMenuWindow:
    def __init__(self, screen_size):
        self.screen_width, self.screen_height = screen_size
        self.window = pygame.transform.scale(pygame.image.load("Assets/white-bg.png"), (int(self.screen_width * 0.4), int(self.screen_height)))
        # player information
        self.player_name = COMIC_SANS18.render("", 1, "#333333")
        self.player_balance = COMIC_SANS18.render("0", 1, "#333333")
        # surface position handling
        self.window_rect = self.window.get_rect()
        self.window_rect.topleft = (int(self.screen_width * 0.6), 0)
        self.player_name_rect = self.player_name.get_rect()
        self.player_name_rect.topleft = (int(self.screen_width * 0.6, 0))
        self.player_balance_rect = self.player_balance.get_rect()
        self.player_name_rect.topleft = (int(self.screen_width * 0.6, 20))
    def updateWidtthPlayer(self, player: Player):
        self.player_name = COMIC_SANS18.render(f'Name: {player.name}', 1, "#333333")
        self.player_balance = COMIC_SANS18.render(f'Name: {player.balance}', 1, "#333333")
        self.player_name_rect = self.player_name.get_rect()
        self.player_name_rect.topleft = (int(self.screen_width * 0.6, 0))
        self.player_balance_rect = self.player_balance.get_rect()
        self.player_name_rect.topleft = (int(self.screen_width * 0.6, 20))
    def renderToScreen(self, screen: pygame.Surface):
        screen.blit(self.window, self.window_rect)
        screen.blit(self.player_name, self.player_name_rect)
        screen.blit(self.player_balance, self.player_balance_rect)
    

        