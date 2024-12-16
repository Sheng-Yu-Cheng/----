from typing import List, Callable
from random import randint
from utilities import *
import pygame

class EventCard:
    def __init__(self, 
            image: pygame.Surface, 
            weight: int, 
            need_block_selection: bool = False, 
            block_target_filter: Callable = lambda x, y, z, w: False, 
            block_target_maxmium: int = 0, 
            need_player_selection: bool = False, 
            player_target_filter: Callable = lambda x, y, z: False,
            player_target_maxmimum: int = 0, 
            effect: Callable = lambda: None
        ):
        self.image = image
        self.rect = image.get_rect()
        self.weight = weight
        #
        self.need_block_selection = need_block_selection
        self.block_target_filter = block_target_filter
        self.block_target_maxmium = block_target_maxmium
        self.need_player_selection = need_player_selection
        self.player_target_filter = player_target_filter
        self.player_target_maxmimum = player_target_maxmimum
        self.selected = False
        #
        self.effect: Callable = effect
    def doEffect(self, block, selected_blocks, board, now_player, selected_players, players):
        self.effect(block, selected_blocks, board, now_player, selected_players, players)
    
class EventCardDeck:
    def __init__(self, deck: List[EventCard]):
        self.deck: List[EventCard] = deck
        self.weight_prefix_sum = [0]
        for card in self.deck:
            self.weight_prefix_sum.append(self.weight_prefix_sum[-1] + card.weight)
        self.total_weight = sum([card.weight for card in self.deck])
        self.now_card = None
    def drawCard(self):
        random_value = randint(1, self.total_weight)
        L, R = 0, len(self.deck) - 1
        while L <= R - 1:
            M = L + R >> 1
            if self.weight_prefix_sum[M] <= random_value:
                R = M
            else:
                L = M + 1
        self.now_card = self.deck[R] if self.weight_prefix_sum[R] <= random_value else self.deck[L]
    def renderToScreen(self, screen: pygame.Surface):
        screen.blit(self.now_card.image, (200, 70))
