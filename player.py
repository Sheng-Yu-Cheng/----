from stock import *
from prop import *
import pygame
from typing import List

class PlayerToken:
    def __init__(self, image: pygame.Surface):
        self.image: pygame.Surface = image
        self.rect: pygame.Rect = image.get_rect()

class Player:
    def __init__(self, 
            name: str, 
            index: int, 
            token: PlayerToken,
            stock_account: StockMarketAccount, 
            props: List[Prop],  
            position: int = 0, 
            balance = 0
        ):
        self.name = name
        self.index = index
        self.position = position
        self.balance = balance
        self.stock_account: StockMarketAccount = stock_account
        self.props: List[Prop] = props
        #
        self.stop_round = 0
        #
        self.token = token
        self.token_position = position
        self.bought_this_round = False
    def renderToScreen(self, screen: pygame.Surface):
        screen.blit(self.token.image, self.token.rect)


