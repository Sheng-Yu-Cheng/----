from block import *
from font_machine import *
from utilities import *
from typing import List, Tuple, Union
import pygame

class ActionMenuWindow:
    def __init__(self, screen_size):
        self.screen_width, self.screen_height = screen_size
        self.window = pygame.transform.scale(pygame.image.load("Assets/white-bg.png"), (int(self.screen_width * 0.9), int(self.screen_height * 0.9)))
        # player information
        self.player_name_tag = COMIC_SANS18.render("Player Name", 1, "#CCCCCC")
        self.player_name = COMIC_SANS18.render(player_name, 1, "#EEEEEE")
        self.player_balance_tag = COMIC_SANS18.render("Balance", 1, "#CCCCCC")
        self.player_balance = COMIC_SANS18.render("0", 1, "#EEEEEE")
        # surface position handling
        self.window_rect = self.window.get_rect()
        self.window_rect.topleft = (int(width * 0.05), int(height * 0.05))
        self.player_name_tag_rect = self.player_name_tag.get_rect()
        self.player_name_rect = self.player_name.get_rect()
        self.player_balance_tag_rect = self.player_balance_tag.get_rect()
        self.player_balance_rect = self.player_balance.get_rect()
    def updateToProperty(self, property: Union[StreetBlock, RailroadBlock, UtilityBlock]):
        pass