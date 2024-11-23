# Example file showing a basic pygame "game loop"
import pygame
from game import *

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

players = [
    Player("Alice", 0, balance = 25000), 
    Player("Bob", 0, balance = 25000),  
    Player("Sean", 0, balance = 25000),  
    Player("Andrew", 0, balance = 25000)
]
game = Game((1280, 720), generateClassicGameBoard(), players)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    game.renderToScreen(screen)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()