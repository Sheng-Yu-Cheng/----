# TODO: delete smortgaging system


# Example file showing a basic pygame "game loop"
import pygame
from game import *

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

player_token = [
    PlayerToken(pygame.image.load("Assets/Player/pink.png")), 
    PlayerToken(pygame.image.load("Assets/Player/orange.png")), 
    PlayerToken(pygame.image.load("Assets/Player/green.png")), 
    PlayerToken(pygame.image.load("Assets/Player/blue.png"))
]
players = [
    Player("Alice", 0, player_token[0], balance = 25000), 
    Player("Bob", 1, player_token[1], balance = 25000), 
    Player("Sean", 2, player_token[2], balance = 25000), 
    Player("Andrew", 3, player_token[3], balance = 25000)
]
market = Market([
    Stock("TSMC", "0"), 
    Stock("Foxconn", "0"), 
    Stock("Delta", "0")
])
game = Game(
    (1280, 720), 
    generateClassicGameBoard(), 
    players, 
    market, 
    GameStatus.WAIT_FOR_ROLLING_DICE)
game.now_player_index = 0
block_collide_list = game.generateCollideRectAndReactFunctionList()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for rect, trigger in block_collide_list:
                if rect.collidepoint(event.pos):
                    trigger()
    if game.status_changed:
        block_collide_list = game.generateCollideRectAndReactFunctionList()
        game.status_changed = False
    game.handleBlockInformationShowing(pygame.mouse.get_pos())
    game.renderToScreen(screen)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()