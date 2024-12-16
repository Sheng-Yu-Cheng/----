from typing import Tuple, Callable, List
from constant import *
import pygame

class Prop:
    def __init__(self, 
        name: str, 
        image: pygame.Surface,
        description = "", 
        need_block_selection: bool = False, 
        block_target_filter: Callable = lambda block, board, now_player_index, players: False, 
        block_target_maximum: int = 0, 
        need_player_selection: bool = False, 
        player_target_filter: Callable = lambda player, board, now_player_index, players: False, 
        player_target_maximum: int = 0, 
        effect: Callable = lambda: None
    ):
        self.name: str = name
        self.image: pygame.Surface = image
        self.rect: pygame.Rect = self.image.get_rect()
        self.description = description
        #
        self.disabled = True
        self.disabled_mask = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        self.disabled_mask.fill((0, 0, 0, 100))
        self.selected = False
        self.selected_mask = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        self.selected_mask.fill((255, 255, 0, 100))
        #
        self.need_block_selection: bool = need_block_selection
        self.block_target_filter: Callable = block_target_filter
        self.block_target_maximum = block_target_maximum
        self.need_player_selection: bool = need_player_selection 
        self.player_target_filter: Callable = player_target_filter
        self.player_target_maximum = player_target_maximum
        self.effect: Callable = effect
    def renderToScreen(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)
        if self.disabled:
            screen.blit(self.disabled_mask, self.rect)
        elif self.selected:
            screen.blit(self.selected_mask, self.rect)
    def setTopleft(self, topleft: Tuple[int]):
        self.rect.topleft = topleft
    def doEffect(self, block, selected_blocks, board, now_player, selected_players, players):
        self.effect(block, selected_blocks, board, now_player, selected_players, players)
    


