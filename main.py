# Example file showing a basic pygame "game loop"
import pygame
from font_machine import *

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

# settings_button = pygame.transform.scale(pygame.image.load("Assets/settings-icon.png"), (50, 50))
# settings_button_rect = settings_button.get_rect()
# settings_button_rect.topleft = (1200, 30)

# settings_window = pygame.transform.scale(pygame.image.load("Assets/settings-page.png"), (400, 500))
# settings_window_rect = settings_window.get_rect()
# settings_window_rect.topleft = (400, 100)
# settings_cancel_button = pygame.transform.scale(pygame.image.load("Assets/cancel.png"), (50, 50))
# settings_cancel_button_rect = settings_cancel_button.get_rect()
# settings_cancel_button_rect.topleft = (350, 0)

# print(settings_cancel_button_rect)

# print(settings_button_rect)

# window_status = "General"


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # elif event.type == pygame.MOUSEBUTTONDOWN:
        #     print(event.pos)
        #     if settings_button_rect.collidepoint(event.pos):
        #         window_status = "Setting"
        #     elif settings_cancel_button_rect.collidepoint(event.pos):
        #         print("LOL")
        #         window_status = "General"

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")
    screen.blit(hello, (500, 500))
    # if window_status == "General":
    #     screen.blit(settings_button, settings_button_rect)
    # elif window_status == "Setting":
    #     settings_window.blit(settings_cancel_button, settings_cancel_button_rect)
    #     screen.blit(settings_window, settings_window_rect)

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()