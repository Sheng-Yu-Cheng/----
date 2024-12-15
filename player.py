from stock import *
from prop import *
import pygame
from typing import List

class PlayerIcon:
    def __init__(self, 
            image: pygame.Surface, 
            topleft: Tuple[int], 
        ):
        self.image = image
        self.rect = image.get_rect()
        self.rect.topleft = topleft
        #
        self.disabled = True
        self.disabled_mask = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        self.disabled_mask.fill((0, 0, 0, 100))
        self.selected = False
        self.selected_mask = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        self.selected_mask.fill((255, 255, 0, 100))
    def renderToScreen(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)
        if self.disabled:
            screen.blit(self.disabled_mask, self.rect)
        elif self.selected:
            screen.blit(self.selected_mask, self.rect)

class PlayerToken:
    def __init__(self, image: pygame.Surface):
        self.image: pygame.Surface = image
        self.rect: pygame.Rect = image.get_rect()

class Player:
    def __init__(self, 
            name: str, 
            index: int, 
            token: PlayerToken,
            icon: PlayerIcon, 
            stock_account: StockMarketAccount, 
            props: List[Prop],  
            position: int = 0, 
            balance = 0, 
            health_point = 100
        ):
        self.name = name
        self.index = index
        self.position = position
        self.balance = balance
        self.health_points = health_point
        self.stock_account: StockMarketAccount = stock_account
        self.props: List[Prop] = props
        #
        self.stop_round = 0
        self.airport_designated_destination = -1
        self.double_steps = False
        self.half_steps = False
        #
        self.icon = icon
        #
        self.token = token
        self.token_position = position
        self.bought_this_round = False
    def renderToScreen(self, screen: pygame.Surface):
        screen.blit(self.token.image, self.token.rect)
        self.icon.renderToScreen(screen)


