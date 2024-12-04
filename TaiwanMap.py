from EventCardDeck import *
from block import *
from constant import *
from player import *
import pygame

# chance card deck
chanceCardDeck = []

# chill guy
image = pygame.image.load("Assets/EventCards/chill guys.jpg")
def chillGuy(block: BLOCK, blocks: list[BLOCK], now_player_index: int, players: list[Player]):
    players[now_player_index].stop_round = 1

chanceCardDeck.append(EventCard(image, 10, False))