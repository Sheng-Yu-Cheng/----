import pygame
from TaiwanMap import *

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

game = generateGame()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for rect, trigger in game.collide_rect_and_react_func_list:
                if rect.collidepoint(event.pos):
                    trigger()
    game.handleBlockInformationShowing(pygame.mouse.get_pos())
    game.renderToScreen(screen)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()