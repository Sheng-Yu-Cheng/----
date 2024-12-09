from utilities import *
from game_board import *
from EventCardDeck import *
from block import *
from constant import *
from player import *
import pygame

# chance card deck
chanceCardDeck = []

# 一百塊
image_1 = pygame.image.load("Assets/EventCards/Chance/一百塊 勒.jpg")
def addOneHundred(block: BLOCK, board: GameBoard, now_player_index: int, players: list[Player]):
    players[now_player_index].balance += 100
chanceCardDeck.append(EventCard(image_1, 10, need_selection=False, effect=addOneHundred))

# 小新的車車
image_2 = pygame.image.load("Assets/EventCards/小新的車車.jpg")
def aCar(block: BLOCK, blocks: list[BLOCK], now_player_index: int, players: list[Player]):
    pass
chanceCardDeck.append(EventCard(image_2, 10, need_selection=False, effect=aCar))

# 出事了阿北
image_3 = pygame.image.load("Assets/EventCards/出事了阿北.jpg")
def kP(block: BLOCK, board: GameBoard, now_player_index: int, players: list[Player]):
    players[now_player_index].position = players[now_player_index].token_position = board.prison_block_index
    now_player = players[now_player_index]
    now_block = board.blocks[board.prison_block_index]
    now_player.stop_round = 3
    now_player.token.rect.topleft = addCoordinates(now_block.rect.center, TOKEN_OFFSET[now_player.index])
chanceCardDeck.append(EventCard(image_3, 10, need_selection=False, effect=kP))

# 外星人
image_4 = pygame.image.load("Assets/EventCards/外星人.jpg")
def aliens(block: BLOCK, board: GameBoard, now_player_index: int, players: list[Player]):
    players[now_player_index].stop_round = 1
chanceCardDeck.append(EventCard(image_4, 5, need_selection=False, effect=aliens))

# 快不行了
image_5 = pygame.image.load("Assets/EventCards/快不行了.jpg")
def scldIsNightmare(block: BLOCK, board: GameBoard, now_player_index: int, players: list[Player]):
    players[now_player_index].balance -= 1000
chanceCardDeck.append(EventCard(image_5, 10, need_selection=False, effect=scldIsNightmare))

# 穿牆術
image_6 = pygame.image.load("Assets/EventCards/穿牆術.jpg")
def passWall(block: BLOCK, board: GameBoard, now_player_index: int, players: list[Player]):
    pass
chanceCardDeck.append(EventCard(image_6, 10, need_selection=False, effect=passWall))

# 野豬騎士
image_7 = pygame.image.load("Assets/EventCards/野豬騎士.jpg")
def hogRider(players, blocks):
    pass
chanceCardDeck.append(EventCard(image_7, 5, need_selection=False, target_filter=True, effect=hogRider))

# 撿到錢包
image_8 = pygame.image.load("Assets/EventCards/撿到錢包.jpg")
def aWallet(block: BLOCK, board: GameBoard, now_player_index: int, players: list[Player]):
    players[now_player_index].balance += 1000
chanceCardDeck.append(EventCard(image_8, 8, need_selection=False, effect=aWallet))

# 幫幫人民的啦
image_9 = pygame.image.load("Assets/EventCards/幫幫人民的啦.jpg")
def giveMoney(block: BLOCK, board: GameBoard, now_player_index: int, players: list[Player]):
    players[now_player_index].balance -= 1000
chanceCardDeck.append(EventCard(image_9, 8, need_selection=False, effect=giveMoney))

# chill guy
image_10 = pygame.image.load("Assets/EventCards/chill guys.jpg")
def chillGuy(block: BLOCK, board: GameBoard, now_player_index: int, players: list[Player]):
    players[now_player_index].stop_round = 1
chanceCardDeck.append(EventCard(image_10, 10, need_selection=False, effect=chillGuy))

# Community Chest Deck
communityChestDeck = []

# 大爆炸
image_11 = pygame.image.load("Assets/EventCards/大爆炸.jpg")
def explosion(players, blocks):
    pass
communityChestDeck.append(EventCard(image_11, 2, need_selection=False, effect=explosion))

# 月光刑警
image_12 = pygame.image.load("Assets/EventCards/月光刑警.jpg")
def moonlightPower(players, blocks):
    pass
communityChestDeck.append(EventCard(image_12, 5, need_selection=False, target_filter=True , effect=moonlightPower))

# 出車禍
image_13 = pygame.image.load("Assets/EventCards/出車禍.jpg")
def michael(players, blocks):
    pass
communityChestDeck.append(EventCard(image_13, 5, need_selection=False, effect=michael))

# 好友基德
image_14 = pygame.image.load("Assets/EventCards/好友基德.jpg")
def goodFreind(players, blocks):
    pass
communityChestDeck.append(EventCard(image_14, 5, need_selection=False, effect=goodFreind))

# 凍蒜
image_15 = pygame.image.load("Assets/EventCards/凍蒜.jpg")
def tiKoLiang(players, blocks):
    pass
communityChestDeck.append(EventCard(image_15, 3, need_selection=False, target_filter=True, effect=tiKoLiang))

# 跌價妖怪女
image_16 = pygame.image.load("Assets/EventCards/跌價妖怪女.jpg")
def Ume(players, blocks):
    pass
communityChestDeck.append(EventCard(image_16, 4, need_selection=False, effect=Ume))

# 檢舉達人
image_17 = pygame.image.load("Assets/EventCards/檢舉達人.jpg")
def reporter(players, blocks):
    pass
communityChestDeck.append(EventCard(image_17, 3, need_selection=True, effect=reporter))

# 魔法小卡
image_18 = pygame.image.load("Assets/EventCards/魔法小卡.jpg")
def creditCard(players, blocks):
    pass
communityChestDeck.append(EventCard(image_18, 3, need_selection=True, effect=creditCard))

# gg
image_19 = pygame.image.load("Assets/EventCards/gg.jpg")
def goodGame(players, blocks):
    pass
communityChestDeck.append(EventCard(image_19, 3, need_selection=False, effect=goodGame))