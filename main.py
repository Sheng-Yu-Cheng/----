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
game = Game((1280, 720), generateClassicGameBoard(), players, GameStatus.SELLING)
game.now_player_index = 0
game.board.blocks[1].owner = 0
game.board.blocks[3].owner = 0
game.board.blocks[5].owner = 0
block_collide_list = game.generateCollideRectAndFunctionList()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for rect, func in block_collide_list:
                if rect.collidepoint(event.pos):
                    func()
    game.handleBlockInformationShowing(pygame.mouse.get_pos())
    game.renderToScreen(screen)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()