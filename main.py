# TODO: mortgaging system


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
    Player("Bob", 1, balance = 25000), 
    Player("Sean", 2, balance = 25000), 
    Player("Andrew", 3, balance = 25000)
]
game = Game((1280, 720), generateClassicGameBoard(), players, GameStatus.WAIT_FOR_ROLLING_DICE)
game.now_player_index = 0
block_collide_list = game.generateCollideRectAndFunctionList()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for rect, trigger in block_collide_list:
                if rect.collidepoint(event.pos):
                    trigger()
    if game.status_changed:
        block_collide_list = game.generateCollideRectAndFunctionList()
        game.status_changed = False
    game.handleBlockInformationShowing(pygame.mouse.get_pos())
    game.renderToScreen(screen)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()