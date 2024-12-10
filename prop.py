from typing import Tuple
import pygame

class Prop:
    def __init__(self, 
        name: str, 
        image: pygame.Surface,
        need_selection: bool
        
    ):
        self.name: str = name
        self.image: pygame.Surface = image
        self.rect: pygame.Rect = self.image.get_rect()
    def renderToScreen(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)
    def setTopleft(self, topleft: Tuple[int]):
        self.rect.topleft = topleft
    