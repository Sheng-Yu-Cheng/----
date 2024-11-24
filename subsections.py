from block import *
from player import *
from font_machine import *
from utilities import *
from constant import *
from typing import List, Tuple, Union
import pygame

class ActionMenuWindow:
    def __init__(self, screen_size):
        self.screen_width, self.screen_height = screen_size
        self.window = pygame.transform.scale(pygame.image.load("Assets/action menu/white.png"), (int(self.screen_width * 0.4), int(self.screen_height / 2)))
        # player information
        self.player_name = COMIC_SANS18.render("Name: ", 1, "#000000")
        self.player_balance = COMIC_SANS18.render("Balance: ", 1, "#000000")
        # buttons
        self.sell_button = COMIC_SANS18.render("-SELL-", 1, "#000000", "#FFFF00")
        self.mortagage_button = COMIC_SANS18.render("-MORTAGAGE-", 1, "#000000", "#FFFF00")
        self.confirm_button = COMIC_SANS18.render("-CONFIRM-", 1, "#000000", "#00FF00")
        self.cancel_button = COMIC_SANS18.render("-CANCEL-", 1, "#000000", "#FF0000")
        # surface position handling
        self.window_rect = self.window.get_rect()
        self.window_rect.topleft = (int(self.screen_width * 0.6), 0)
        self.player_name_rect = self.player_name.get_rect()
        self.player_name_rect.topleft = (int(self.screen_width * 0.6), 0)
        self.player_balance_rect = self.player_balance.get_rect()
        self.player_balance_rect.topleft = (int(self.screen_width * 0.6), 20)
        self.sell_button_rect = self.sell_button.get_rect()
        self.sell_button_rect.topleft = (int(self.screen_width * 0.6), 40)
        self.mortagage_button_rect = self.mortagage_button.get_rect()
        self.mortagage_button_rect.topleft = (int(self.screen_width * 0.6) + self.sell_button_rect.width + 5, 40)
        self.confirm_button_rect = self.confirm_button.get_rect()
        self.confirm_button_rect.topleft = (int(self.screen_width * 0.6), 40)
        self.cancel_button_rect = self.cancel_button.get_rect()
        self.cancel_button_rect.topleft = (int(self.screen_width * 0.6) + self.sell_button_rect.width + 5, 40)
    def updateWithPlayer(self, player: Player):
        self.player_name = COMIC_SANS18.render(f'Name: {player.name}', 1, "#000000")
        self.player_balance = COMIC_SANS18.render(f'Balance: {player.balance}', 1, "#000000")
        self.player_name_rect = self.player_name.get_rect()
        self.player_name_rect.topleft = (int(self.screen_width * 0.6), 0)
        self.player_balance_rect = self.player_balance.get_rect()
        self.player_balance_rect.topleft = (int(self.screen_width * 0.6), 20)
    def renderToScreen(self, screen: pygame.Surface, game_status):
        screen.blit(self.window, self.window_rect)
        screen.blit(self.player_name, self.player_name_rect)
        screen.blit(self.player_balance, self.player_balance_rect)
        screen.blit(self.sell_button, self.sell_button_rect)
        screen.blit(self.mortagage_button, self.mortagage_button_rect)

class BlockInformation:
    def __init__(self, screen_size):
        self.screen_width, self.screen_height = screen_size
        self.window = pygame.transform.scale(pygame.image.load("Assets/action menu/white.png"), (int(self.screen_width * 0.4), int(self.screen_height / 2)))
        self.window_rect = self.window.get_rect()
        self.window_rect.topleft = (int(self.screen_width * 0.6), int(self.screen_height / 2))
        #
        self.block_name = COMIC_SANS18.render("", 1, "#000000")
        self.block_name_rect = self.block_name.get_rect()
        self.block_name_rect.topleft = (int(self.screen_width * 0.6), int(self.screen_height / 2))
        #
        self.block_owner = COMIC_SANS18.render("", 1, "#000000")
        self.block_owner_rect = self.block_owner.get_rect()
        self.block_owner_rect.topleft = (int(self.screen_width * 0.6), int(self.screen_height / 2) + 20)
        #
        self.additional_information : List[Tuple[pygame.Surface, pygame.Rect]] = []
    def updateToBlock(self, block: BLOCK):
        self.block_name = COMIC_SANS18.render(block.name, 1, "#000000")
        self.additional_information = []
        if block.type == BlockType.STREET:
            self.block_owner = COMIC_SANS18.render(f"Owner: {block.owner}", 1, "#000000")
            self.block_owner_rect = self.block_owner.get_rect()
            self.block_name_rect.topleft = (int(self.screen_width * 0.6), int(self.screen_height / 2) + 20)
    def renderToScreen(self, screen: pygame.Surface):
        screen.blit(self.window, self.window_rect)
        screen.blit(self.block_name, self.block_name_rect)
        screen.blit(self.block_owner, self.block_owner_rect)
