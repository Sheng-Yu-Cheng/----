from utilities import *
from font_machine import *
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
        self.invisible_round = False
        self.half_steps = False
        self.identification = -1
        #
        self.icon = icon
        #
        self.token = token
        self.token_position = position
        self.bought_this_round = False
        self.health_points_text = COMIC_SANS18.render(f"{self.health_points}/100", 1, "#FFFFFF")
    def decreaseHealthPoint(self, amount):
        self.health_points -= amount
        if self.health_points <= 0:
            self.stop_round = 2
        self.health_points_text = COMIC_SANS18.render(f"{self.health_points}/100", 1, "#FFFFFF")
    def stopRoundCountDown(self):
        if self.stop_round > 0:
            self.stop_round -= 1
            if self.stop_round == 0 and self.health_points <= 0:
                self.health_points = 100
                self.health_points_text = COMIC_SANS18.render(f"{self.health_points}/100", 1, "#FFFFFF")
    def renderToScreen(self, screen: pygame.Surface):
        screen.blit(self.token.image, self.token.rect)
        self.icon.renderToScreen(screen)
        screen.blit(self.health_points_text, addCoordinates(self.icon.rect, (0, 40)))


