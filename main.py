# Example file showing a basic pygame "game loop"
import pygame
from subwindows import *
from font_machine import *

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

action_menu = ActionMenuWindow((1280, 720))


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill("purple")
    
    
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()