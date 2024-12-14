from typing import Tuple, Callable, List
import pygame

class Prop:
    def __init__(self, 
        name: str, 
        image: pygame.Surface,
        need_block_selection: bool = False, 
        block_target_filter: Callable = lambda: None, 
        need_player_selection: bool = False, 
        player_target_filter: Callable = lambda: None, 
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
        self.need_player_selection: bool = need_player_selection 
        self.player_target_filter: Callable = player_target_filter
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
    return Prop("Bomb", pygame.transform.scale(pygame.image.load("Assets/TaiwanBoard/Props/Bomb.png"), (200,50)), need_player_selection=True, player_target_filter=lambda x, y, z:True, block_target_filter=lambda x, y, z, w: False, effect = bomb)

