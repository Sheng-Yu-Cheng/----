import pygame
from TaiwanMap import *

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

game = generateGame()
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