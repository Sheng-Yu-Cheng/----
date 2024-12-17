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
    mouse_pos = pygame.mouse.get_pos()
    game.handleBlockInformationShowing(mouse_pos)
    game.handlePropInformationShowing(mouse_pos)
    screen.fill((0, 0, 0))
    game.renderToScreen(screen)
    if game.game_over:
        screen.fill((0, 0, 0))
        HUNINN50.render(f"遊戲結束，玩家{game.now_player_index}輸了", 1, "#FFFFFF")
        running = False   
    pygame.display.flip()
    clock.tick(60)


clock.tick(5000)
pygame.quit() 