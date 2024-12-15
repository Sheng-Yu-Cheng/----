from typing import Tuple, Callable, List
from constant import *
import pygame

class Prop:
    def __init__(self, 
        name: str, 
        image: pygame.Surface,
        need_block_selection: bool = False, 
        block_target_filter: Callable = lambda: None, 
        block_target_maximum: int = 0, 
        need_player_selection: bool = False, 
        player_target_filter: Callable = lambda: None, 
        player_target_maximum: int = 0, 
        effect: Callable = lambda: None
    ):
        self.name: str = name
        self.image: pygame.Surface = image
        self.rect: pygame.Rect = self.image.get_rect()
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
    

def Bomb() -> Prop:
    def bomb(block, selected_blocks, board, now_player, selected_players, players):
        for player in selected_players:
            player.health_points -= 40
            if player.health_points <= 0:
                player.stop_round = 3
                player.health_points = 100
    return Prop(
        "Bomb", 
        pygame.transform.scale(pygame.image.load("Assets/TaiwanBoard/Props/Gernade.jpg"), (240, 320)), 
        need_player_selection = True, 
        player_target_filter = lambda x, y, z:True, 
        player_target_maximum = 1, 
        block_target_filter = lambda x, y, z, w: False, 
        block_target_maximum = 0, 
        effect = bomb
    )

def Barrier() -> Prop:
    def setBarrier(block, selected_blocks: List[BLOCK], board, now_player, selected_players, players):
        if len(selected_blocks) == 1:
            selected_blocks[0].has_barrier = True
    return Prop(
        "Barrier", 
        pygame.transform.scale(pygame.image.load("Assets/TaiwanBoard/Props/Barrier.jpg"), (240, 320)), 
        need_player_selection = False, 
        player_target_filter = lambda x, y, z:False, 
        player_target_maximum = 0, 
        need_block_selection = True, 
        block_target_filter = lambda x, y, z, w: True, 
        block_target_maximum = 1, 
        effect = setBarrier
    )

def Rabbit() -> Prop:
    def rabbit(block, selected_blocks: List[BLOCK], board, now_player, selected_players, players):
        now_player.double_steps = True
    return Prop(
        "Rabbit", 
        pygame.transform.scale(pygame.image.load("Assets/TaiwanBoard/Props/Barrier.jpg"), (240, 320)), 
        need_player_selection = False, 
        player_target_filter = lambda x, y, z:False, 
        player_target_maximum = 0, 
        need_block_selection = False, 
        block_target_filter = lambda x, y, z, w: False, 
        block_target_maximum = 1, 
        effect = rabbit
    )

def Turtle() -> Prop:
    def turtle(block, selected_blocks: List[BLOCK], board, now_player, selected_players, players):
        now_player.half_steps = True
    return Prop(
        "Trutle", 
        pygame.transform.scale(pygame.image.load("Assets/TaiwanBoard/Props/Barrier.jpg"), (240, 320)), 
        need_player_selection = False, 
        player_target_filter = lambda x, y, z:False, 
        player_target_maximum = 0, 
        need_block_selection = False, 
        block_target_filter = lambda x, y, z, w: False, 
        block_target_maximum = 1, 
        effect = turtle
    )