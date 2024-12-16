from utilities import *
from game import *
from EventCardDeck import *
from block import *
from constant import *
from player import *
import pygame


def Pistol() -> Prop:
    def pistol(block, selected_blocks, board, now_player, selected_players: List[Player], players):
        for player in selected_players:
            player.decreaseHealthPoint(40)
    return Prop(
        "Pistol", 
        pygame.transform.scale(pygame.image.load("Assets/TaiwanBoard/Props/Pistol.jpg"), (240, 320)), 
        need_player_selection = True, 
        player_target_filter = lambda x, y, z:True, 
        player_target_maximum = 1, 
        block_target_filter = lambda x, y, z, w: False, 
        block_target_maximum = 0, 
        effect = pistol
    )

def Barrier() -> Prop:
    def setBarrier(block, selected_blocks: List[BLOCK], board, now_player, selected_players, players):
        if len(selected_blocks) == 1:
            selected_blocks[0].has_barrier = True
    return Prop(
        "Barrier", 
        pygame.transform.scale(pygame.image.load("Assets/TaiwanBoard/Props/Barrier.jpg"), (240, 320)), 
        need_player_selection = False, 
        player_target_filter = lambda x, y, z:False, 
        player_target_maximum = 0, 
        need_block_selection = True, 
        block_target_filter = lambda x, y, z, w: True, 
        block_target_maximum = 1, 
        effect = setBarrier
    )

def Rabbit() -> Prop:
    def rabbit(block, selected_blocks: List[BLOCK], board, now_player, selected_players, players):
        now_player.double_steps = True
    return Prop(
        "Rabbit", 
        pygame.transform.scale(pygame.image.load("Assets/TaiwanBoard/Props/Rabbit.jpg"), (240, 320)), 
        need_player_selection = False, 
        player_target_filter = lambda x, y, z:False, 
        player_target_maximum = 0, 
        need_block_selection = False, 
        block_target_filter = lambda x, y, z, w: False, 
        block_target_maximum = 1, 
        effect = rabbit
    )

def Turtle() -> Prop:
    def turtle(block, selected_blocks: List[BLOCK], board, now_player, selected_players, players):
        now_player.half_steps = True
    return Prop(
        "Trutle", 
        pygame.transform.scale(pygame.image.load("Assets/TaiwanBoard/Props/Turtle.jpg"), (240, 320)), 
        need_player_selection = False, 
        player_target_filter = lambda x, y, z:False, 
        player_target_maximum = 0, 
        need_block_selection = False, 
        block_target_filter = lambda x, y, z, w: False, 
        block_target_maximum = 1, 
        effect = turtle
    )

def Bomb() -> Prop:
    def bomb(block, selected_blocks: List[BLOCK], board, now_player, selected_players, players):
        block.has_bomb = True
    return Prop(
        "Trutle", 
        pygame.transform.scale(pygame.image.load("Assets/TaiwanBoard/Props/Gernade.jpg"), (240, 320)), 
        need_player_selection = False, 
        player_target_filter = lambda x, y, z:False, 
        player_target_maximum = 0, 
        need_block_selection = False, 
        block_target_filter = lambda x, y, z, w: False, 
        block_target_maximum = 0, 
        effect = bomb
    )

def Lord() -> Prop:
    def lord(block: BLOCK, selected_blocks: List[BLOCK], board: GameBoard, now_player: Player, selected_players: List[Player], players: list[Player]):
        selected_blocks[0].owner = now_player.index
    def filter(block, board, now_player_index, players):
        return isinstance(block, PROPERTY_BLCOK) and block.owner != now_player_index
    return Prop(
        "Trutle", 
        pygame.transform.scale(pygame.image.load("Assets/TaiwanBoard/Props/Lord.jpg"), (240, 320)), 
        need_player_selection = False, 
        player_target_filter = lambda x, y, z:False, 
        player_target_maximum = 0, 
        need_block_selection = True, 
        block_target_filter = filter, 
        block_target_maximum = 1, 
        effect = lord
    )

def Digger() -> Prop:
    def digger(block: BLOCK, selected_blocks: List[BLOCK], board: GameBoard, now_player: Player, selected_players: List[Player], players: list[Player]):
        selected_blocks[0].house_amount = 0
    def filter(block, board, now_player_index, players):
        return isinstance(block, PROPERTY_BLCOK) and block.owner != now_player_index
    return Prop(
        "Trutle", 
        pygame.transform.scale(pygame.image.load("Assets/TaiwanBoard/Props/Digger.jpg"), (240, 320)), 
        need_player_selection = False, 
        player_target_filter = lambda x, y, z:False, 
        player_target_maximum = 0, 
        need_block_selection = True, 
        block_target_filter = filter, 
        block_target_maximum = 1, 
        effect = digger
    )

# TODO
def CreditCard() ->Prop:
    pass

def generateGame() -> Game:
    # chance card deck
    chance_card_deck_list = []

    # 一百塊
    image_1 = pygame.transform.scale(pygame.image.load("Assets/EventCards/Chance/一百塊 勒.jpg"), (500, 725))
    def addOneHundred(block: BLOCK, selected_blocks: List[BLOCK], board: GameBoard, now_player: Player, selected_players: List[Player], players: list[Player]):
        now_player.balance += 100
    chance_card_deck_list.append(EventCard(image_1, 10, effect=addOneHundred))

    # 小新的車車
    image_2 = pygame.transform.scale(pygame.image.load("Assets/EventCards/Chance/小新的車車.jpg"), (500, 725))
    def aCar(block: BLOCK, selected_blocks: List[BLOCK], board: GameBoard, now_player: Player, selected_players: List[Player], players: list[Player]):
        if len(now_player.props) <= 4:
            now_player.props.append(Rabbit())
    chance_card_deck_list.append(EventCard(image_2, 10, effect=aCar))

    # 出事了阿北
    image_3 = pygame.transform.scale(pygame.image.load("Assets/EventCards/Chance/出事了阿北.jpg"), (500, 725))
    def kP(block: BLOCK, selected_blocks: List[BLOCK], board: GameBoard, now_player: Player, selected_players: List[Player], players: list[Player]):
        now_player.position = now_player.token_position = board.prison_block_index
        now_block = board.blocks[board.prison_block_index]
        now_player.stop_round = 3
        now_player.token.rect.topleft = addCoordinates(now_block.rect.center, TOKEN_OFFSET[now_player.index])
    chance_card_deck_list.append(EventCard(image_3, 10, effect=kP))

    # 外星人
    image_4 = pygame.transform.scale(pygame.image.load("Assets/EventCards/Chance/外星人.jpg"), (500, 725))
    def aliens(block: BLOCK, selected_blocks: List[BLOCK], board: GameBoard, now_player: Player, selected_players: List[Player], players: list[Player]):
        now_player.stop_round = 1
    chance_card_deck_list.append(EventCard(image_4, 5, effect=aliens))

    # 快不行了
    image_5 = pygame.transform.scale(pygame.image.load("Assets/EventCards/Chance/快不行了.jpg"), (500, 725))
    def scldIsNightmare(block: BLOCK, selected_blocks: List[BLOCK], board: GameBoard, now_player: Player, selected_players: List[Player], players: list[Player]):
        now_player.balance -= 1000
    chance_card_deck_list.append(EventCard(image_5, 10, effect=scldIsNightmare))

    # 穿牆術
    image_6 = pygame.transform.scale(pygame.image.load("Assets/EventCards/Chance/穿牆術.jpg"), (500, 725))
    def passWall(block: BLOCK, selected_blocks: List[BLOCK], board: GameBoard, now_player: Player, selected_players: List[Player], players: list[Player]):
        now_player.invisible_round = True
    chance_card_deck_list.append(EventCard(image_6, 10, effect=passWall))

    # 野豬騎士
    image_7 = pygame.transform.scale(pygame.image.load("Assets/EventCards/Chance/野豬騎士.jpg"), (500, 725))
    def hogRider(block: BLOCK, selected_blocks: List[BLOCK], board: GameBoard, now_player: Player, selected_players: List[Player], players: list[Player]):
        selected_blocks[0].owner = now_player.index
    def hogRiderBlockTargetFilter(block, board, now_player_index, players):
        return isinstance(block, BLOCK) and block.owner != now_player_index
    chance_card_deck_list.append(EventCard(image_7, 5, need_block_selection=True, block_target_filter = hogRiderBlockTargetFilter, block_target_maxmium=1, effect=hogRider))

    # 撿到錢包
    image_8 = pygame.transform.scale(pygame.image.load("Assets/EventCards/Chance/撿到錢包.jpg"), (500, 725))
    def aWallet(block: BLOCK, selected_blocks: List[BLOCK], board: GameBoard, now_player: Player, selected_players: List[Player], players: list[Player]):
        now_player.balance += 1000
    chance_card_deck_list.append(EventCard(image_8, 8, effect=aWallet))

    # 幫幫人民的啦
    image_9 = pygame.transform.scale(pygame.image.load("Assets/EventCards/Chance/幫幫人民的啦.jpg"), (500, 725))
    def giveMoney(block: BLOCK, selected_blocks: List[BLOCK], board: GameBoard, now_player: Player, selected_players: List[Player], players: list[Player]):
        now_player.balance -= 1000
    chance_card_deck_list.append(EventCard(image_9, 8, effect=giveMoney))

    # chill guy
    image_10 = pygame.transform.scale(pygame.image.load("Assets/EventCards/chance/chill guy.jpg"), (500, 725))
    def chillGuy(block: BLOCK, selected_blocks: List[BLOCK], board: GameBoard, now_player: Player, selected_players: List[Player], players: list[Player]):
        now_player.stop_round = 1
    chance_card_deck_list.append(EventCard(image_10, 10, effect=chillGuy))

    # Community Chest Deck
    community_chest_deck_list = []

    # 大爆炸
    image_11 = pygame.transform.scale(pygame.image.load("Assets/EventCards/CommunityChest/大爆炸.jpg"), (500, 725))
    def explosion(block: BLOCK, selected_blocks: List[BLOCK], board: GameBoard, now_player: Player, selected_players: List[Player], players: list[Player]):
        for blk in board.blocks:
            blk.house_amount = 0
    community_chest_deck_list.append(EventCard(image_11, 2, effect=explosion))

    # 月光刑警
    image_12 = pygame.transform.scale(pygame.image.load("Assets/EventCards/CommunityChest/月光刑警.jpg"), (500, 725))
    def moonlightPower(block: BLOCK, selected_blocks: List[BLOCK], board: GameBoard, now_player: Player, selected_players: List[Player], players: list[Player]):
        now_player.token_position = now_player.position = selected_blocks[0].index
        now_block = board.blocks[board.prison_block_index]
        now_player.token.rect.topleft = addCoordinates(now_block.rect.center, TOKEN_OFFSET[now_player.index])
    def moonlightPowerBlockTargetFilter(block, board, now_player_index, players):
        return True
    community_chest_deck_list.append(EventCard(image_12, 5, need_block_selection=True, block_target_filter=moonlightPowerBlockTargetFilter, block_target_maxmium=1 , effect=moonlightPower))

    # 出車禍
    image_13 = pygame.transform.scale(pygame.image.load("Assets/EventCards/CommunityChest/出車禍.jpg"), (500, 725))
    def michael(block: BLOCK, selected_blocks: List[BLOCK], board: GameBoard, now_player: Player, selected_players: List[Player], players: list[Player]):
        now_player.stop_round = 2
    community_chest_deck_list.append(EventCard(image_13, 5, effect=michael))

    # 好友基德
    image_14 = pygame.transform.scale(pygame.image.load("Assets/EventCards/CommunityChest/好友基德.jpg"), (500, 725))
    def goodFreind(block: BLOCK, selected_blocks: List[BLOCK], board: GameBoard, now_player: Player, selected_players: List[Player], players: list[Player]):
        now_player.balance += randint(10000, 20000)
    community_chest_deck_list.append(EventCard(image_14, 5, effect=goodFreind))

    # 凍蒜
    image_15 = pygame.transform.scale(pygame.image.load("Assets/EventCards/CommunityChest/凍蒜.jpg"), (500, 725))
    def tiKoLiang(block: BLOCK, selected_blocks: List[BLOCK], board: GameBoard, now_player: Player, selected_players: List[Player], players: list[Player]):
        now_player.balance += randint(5000, 25000)
    community_chest_deck_list.append(EventCard(image_15, 3, effect=tiKoLiang))

    # 跌價妖怪女
    image_16 = pygame.transform.scale(pygame.image.load("Assets/EventCards/CommunityChest/跌價妖怪女.jpg"), (500, 725))
    def Ume(block: BLOCK, selected_blocks: List[BLOCK], board: GameBoard, now_player: Player, selected_players: List[Player], players: list[Player]):
        now_player.balance >>= 1
    community_chest_deck_list.append(EventCard(image_16, 4, effect=Ume))

    # 檢舉達人
    image_17 = pygame.transform.scale(pygame.image.load("Assets/EventCards/CommunityChest/檢舉達人.jpg"), (500, 725))
    def reporter(block: BLOCK, selected_blocks: List[BLOCK], board: GameBoard, now_player: Player, selected_players: List[Player], players: list[Player]):
        now_player.position = now_player.token_position = board.prison_block_index
        now_block = board.blocks[board.prison_block_index]
        now_player.stop_round = 3
        now_player.token.rect.topleft = addCoordinates(now_block.rect.center, TOKEN_OFFSET[now_player.index])
    community_chest_deck_list.append(EventCard(image_17, 3, need_player_selection=True, player_target_filter= lambda x, y, z: True,player_target_maxmimum=1 , effect=reporter))

    # 魔法小卡
    image_18 = pygame.transform.scale(pygame.image.load("Assets/EventCards/CommunityChest/魔法小卡.jpg"), (500, 725))
    def creditCard(block: BLOCK, selected_blocks: List[BLOCK], board: GameBoard, now_player: Player, selected_players: List[Player], players: list[Player]):
        now_player.props.append(CreditCard())
    community_chest_deck_list.append(EventCard(image_18, 3, effect=creditCard))

    # gg
    image_19 = pygame.transform.scale(pygame.image.load("Assets/EventCards/CommunityChest/gg.jpg"), (500, 725))
    def goodGame(block: BLOCK, selected_blocks: List[BLOCK], board: GameBoard, now_player: Player, selected_players: List[Player], players: list[Player]):
        for blk in board.blocks:
            if isinstance(blk, PROPERTY_BLCOK) and blk.owner == now_player.index:
                blk.owner = None
                blk.house_amount = 0
        now_player.balance = 25000
        now_player.props.clear()
    community_chest_deck_list.append(EventCard(image_19, 3, effect=goodGame))

    chance_card_deck = EventCardDeck(chance_card_deck_list)
    community_chest_deck = EventCardDeck(community_chest_deck_list)

    ## 

    board = GameBoard()
    icons = [pygame.transform.scale(pygame.image.load("Assets/TaiwanBoard/raw/Default.png"), (300, 400)) for i in range(40)]
    #
    go_image = pygame.image.load("Assets/Classic Board/corner.png")
    go = StartBlock(go_image, "Go", 0, 200)
    go.rect.topleft = (640, 640)
    board.addBlock(go)
    #
    guishan_island_image = pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/GuishanIsland.jpg"), -90)
    guishan_island = StreetBlock(pygame.transform.scale(guishan_island_image, (60, 80)), "Block 2", 1, 60, 30, [100, 100, 100, 100, 100], [20, 50, 80, 110, 200, 500], "red",0)
    guishan_island.rect.topleft = (580,640)
    icons[1] = pygame.transform.scale(guishan_island_image, (300, 400))
    board.addBlock(guishan_island)
    #
    commuity_chest1_image = pygame.image.load("Assets/Classic Board/event.png")
    commuity_chest1 = CommunityChestBlock(commuity_chest1_image, "Commmunity Chest", 2, community_chest_deck)
    commuity_chest1.rect.topleft = (520, 640)
    board.addBlock(commuity_chest1)
    #
    block3_image=pygame.image.load("Assets/Classic Board/red.png")
    block3=StreetBlock(block3_image, "Block 3", 3, 60, 30, [100, 100, 100, 100, 100], [20, 50, 80, 110, 200, 500], "red",0)
    block3.rect.topleft = (460, 640)
    board.addBlock(block3)
    #
    income_tax_image = pygame.image.load("Assets/Classic Board/event.png")
    income_tax = IncomeTaxBlock(income_tax_image, "Income Tax", 4, 200)
    income_tax.rect.topleft = (400, 640)
    board.addBlock(income_tax)
    #
    station1_image = pygame.image.load("Assets/Classic Board/event.png")
    station1 = RailroadBlock(station1_image, "Station 1", 5, 200, 100, [50, 100, 200, 400])
    station1.rect.topleft = (340, 640)
    board.addBlock(station1)
    #
    block6_image = pygame.image.load("Assets/Classic Board/light blue.png")
    block6 = StreetBlock(block6_image, "Block 6", 6, 100, 50, [100, 100, 100, 100, 100], [20, 50, 80, 110, 200, 500], "light_blue",0)
    block6.rect.topleft = (280, 640)
    board.addBlock(block6)
    #
    chance1_image = pygame.image.load("Assets/Classic Board/event.png")
    chance1 = ChanceBlock(chance1_image, "Chance", 7, chance_card_deck)
    chance1.rect.topleft = (220, 640)
    board.addBlock(chance1)
    #
    block8_image = pygame.image.load("Assets/Classic Board/light blue.png")
    block8 = StreetBlock(block8_image, "Block 8", 8, 100, 50, [100, 100, 100, 100, 100], [20, 50, 80, 110, 200, 500], "light_blue",0)
    block8.rect.topleft = (160, 640)
    board.addBlock(block8)
    #
    block9_image = pygame.image.load("Assets/Classic Board/light blue.png")
    block9 = StreetBlock(block9_image, "Block 9", 9, 120, 60, [100, 100, 100, 100, 100], [20, 50, 80, 110, 200, 500], "light_blue",0)
    block9.rect.topleft = (100, 640)
    board.addBlock(block9)
    #
    in_jail_or_just_visit_image = pygame.image.load("Assets/Classic Board/corner.png")
    in_jail_or_just_visit = InJailOrJustVisitingBlock(in_jail_or_just_visit_image, "In Jail/Just Visiting", 10)
    in_jail_or_just_visit.rect.topleft = (20, 640)
    board.addBlock(in_jail_or_just_visit)
    #
    block11_image = pygame.transform.rotate(pygame.image.load("Assets/Classic Board/purple.png"), 270)
    block11 = StreetBlock(block11_image, "Block 11", 11, 140, 70, [100, 100, 100, 100, 100], [20, 50, 80, 110, 200, 500], "purple",0)
    block11.rect.topleft = (20, 580)
    board.addBlock(block11)
    #
    utility1_image = pygame.transform.rotate(pygame.image.load("Assets/Classic Board/event.png"), 270)
    utility1 = UtilityBlock(utility1_image, "Electric Company", 12, 150, 75, [100, 250])
    utility1.rect.topleft = (20, 520)
    board.addBlock(utility1)
    #
    block13_image = pygame.transform.rotate(pygame.image.load("Assets/Classic Board/purple.png"), 270)
    block13 = StreetBlock(block13_image, "Block 13", 13, 140, 70, [100, 100, 100, 100, 100], [20, 50, 80, 110, 200, 500], "purple",0)
    block13.rect.topleft = (20, 460)
    board.addBlock(block13)
    #
    block14_image = pygame.transform.rotate(pygame.image.load("Assets/Classic Board/purple.png"), 270)
    block14 = StreetBlock(block14_image, "Block 14", 14, 160, 80, [100, 100, 100, 100, 100], [20, 50, 80, 110, 200, 500], "purple",0)
    block14.rect.topleft = (20, 400)
    board.addBlock(block14)
    #
    station2_image = pygame.transform.rotate(pygame.image.load("Assets/Classic Board/event.png"), 270)
    station2 = RailroadBlock(station2_image, "Station 2", 15, 200, 100, [50, 100, 200, 400])
    station2.rect.topleft = (20, 340)
    board.addBlock(station2)
    #
    block16_image = pygame.transform.rotate(pygame.image.load("Assets/Classic Board/light green.png"), 270)
    block16 = StreetBlock(block16_image, "Block 16", 16, 180, 90, [100, 100, 100, 100, 100], [20, 50, 80, 110, 200, 500], "light_green",0)
    block16.rect.topleft = (20, 280)
    board.addBlock(block16)
    #
    commuity_chest2_image = pygame.transform.rotate(pygame.image.load("Assets/Classic Board/event.png"), 270)
    commuity_chest2 = CommunityChestBlock(commuity_chest2_image, "Commmunity Chest", 17, community_chest_deck)
    commuity_chest2.rect.topleft = (20, 220)
    board.addBlock(commuity_chest2)
    #
    block18_image = pygame.transform.rotate(pygame.image.load("Assets/Classic Board/light green.png"), 270)
    block18 = StreetBlock(block18_image, "Block 18", 18, 180, 90, [100, 100, 100, 100, 100], [20, 50, 80, 110, 200, 500], "light_green",0)
    block18.rect.topleft = (20, 160)
    board.addBlock(block18)
    #
    block19_image = pygame.transform.rotate(pygame.image.load("Assets/Classic Board/light green.png"), 270)
    block19 = StreetBlock(block19_image, "Block 19", 19, 200, 100, [100, 100, 100, 100, 100], [20, 50, 80, 110, 200, 500], "light_green",0)
    block19.rect.topleft = (20, 100)
    board.addBlock(block19)
    #
    free_parking_image = pygame.image.load("Assets/Classic Board/corner.png")
    free_parking = FreeParkingBlock(free_parking_image, "Free Parking", 20, 0)
    free_parking.rect.topleft = (20, 20)
    board.addBlock(free_parking)
    #
    block21_image = pygame.transform.rotate(pygame.image.load("Assets/Classic Board/orange.png"), 180)
    block21 = StreetBlock(block21_image, "Block 21", 21, 220, 110, [100, 100, 100, 100, 100], [20, 50, 80, 110, 200, 500], "orange",0)
    block21.rect.topleft = (100, 20)
    board.addBlock(block21)
    #
    chance2_image = pygame.transform.rotate(pygame.image.load("Assets/Classic Board/event.png"), 180)
    chance2 = ChanceBlock(chance2_image, "Chance", 22, chance_card_deck)
    chance2.rect.topleft = (160, 20)
    board.addBlock(chance2)
    #
    block23_image = pygame.transform.rotate(pygame.image.load("Assets/Classic Board/orange.png"), 180)
    block23 = StreetBlock(block23_image, "Block 23", 23, 220, 110, [100, 100, 100, 100, 100], [20, 50, 80, 110, 200, 500], "orange",0)
    block23.rect.topleft = (220, 20)
    board.addBlock(block23)
    #
    block24_image = pygame.transform.rotate(pygame.image.load("Assets/Classic Board/orange.png"), 180)
    block24 = StreetBlock(block24_image, "Block 24", 24, 240, 120, [100, 100, 100, 100, 100], [20, 50, 80, 110, 200, 500], "orange",0)
    block24.rect.topleft = (280, 20)
    board.addBlock(block24)
    #
    station3_image = pygame.transform.rotate(pygame.image.load("Assets/Classic Board/event.png"), 180)
    station3 = RailroadBlock(station3_image, "Station 3", 25, 200, 100, [50, 100, 200, 400])
    station3.rect.topleft = (340, 20)
    board.addBlock(station3)
    #
    block26_image = pygame.transform.rotate(pygame.image.load("Assets/Classic Board/yellow.png"), 180)
    block26 = StreetBlock(block26_image, "Block 26", 26, 260, 130, [100, 100, 100, 100, 100], [20, 50, 80, 110, 200, 500], "yellow",0)
    block26.rect.topleft = (400, 20)
    board.addBlock(block26)
    #
    block27_image = pygame.transform.rotate(pygame.image.load("Assets/Classic Board/yellow.png"), 180)
    block27 = StreetBlock(block27_image, "Block 27", 27, 260, 130, [100, 100, 100, 100, 100], [20, 50, 80, 110, 200, 500], "yellow",0)
    block27.rect.topleft = (460, 20)
    board.addBlock(block27)
    #
    utility2_image = pygame.transform.rotate(pygame.image.load("Assets/Classic Board/event.png"), 180)
    utility2 = UtilityBlock(utility2_image, "Water Works", 28, 150, 75, [100, 250])
    utility2.rect.topleft = (520, 20)
    board.addBlock(utility2)
    #
    block29_image = pygame.transform.rotate(pygame.image.load("Assets/Classic Board/yellow.png"), 180)
    block29 = StreetBlock(block29_image, "Block 29", 29, 280, 140, [100, 100, 100, 100, 100], [20, 50, 80, 110, 200, 500], "yellow",0)
    block29.rect.topleft = (580, 20)
    board.addBlock(block29)
    #
    go_to_jail_image = pygame.image.load("Assets/Classic Board/corner.png")
    go_to_jail = ImprisonBlock(go_to_jail_image, "Go To Jail", 30)
    go_to_jail.rect.topleft = (640, 20)
    board.addBlock(go_to_jail)
    #
    block31_image = pygame.transform.rotate(pygame.image.load("Assets/Classic Board/green.png"), 90)
    block31 = StreetBlock(block31_image, "Block 31", 31, 300, 150, [100, 100, 100, 100, 100], [20, 50, 80, 110, 200, 500], "green",0)
    block31.rect.topleft = (640, 100)
    board.addBlock(block31)
    #
    block32_image = pygame.transform.rotate(pygame.image.load("Assets/Classic Board/green.png"), 90)
    block32 = StreetBlock(block32_image, "Block 32", 32, 300, 150, [100, 100, 100, 100, 100], [20, 50, 80, 110, 200, 500], "green",0)
    block32.rect.topleft = (640, 160)
    board.addBlock(block32)
    #
    commuity_chest3_image = pygame.transform.rotate(pygame.image.load("Assets/Classic Board/event.png"), 90)
    commuity_chest3 = CommunityChestBlock(commuity_chest3_image, "Commmunity Chest", 33, community_chest_deck)
    commuity_chest3.rect.topleft = (640, 220)
    board.addBlock(commuity_chest3)
    #
    block34_image = pygame.transform.rotate(pygame.image.load("Assets/Classic Board/green.png"), 90)
    block34 = StreetBlock(block34_image, "Block 34", 34, 320, 160, [100, 100, 100, 100, 100], [20, 50, 80, 110, 200, 500], "green",0)
    block34.rect.topleft = (640, 280)
    board.addBlock(block34)
    #
    station4_image = pygame.transform.rotate(pygame.image.load("Assets/Classic Board/event.png"), 90)
    station4 = RailroadBlock(station4_image, "Station 4", 35, 200, 100, [50, 100, 200, 400])
    station4.rect.topleft = (640, 340)
    board.addBlock(station4)
    #
    chance3_image = pygame.transform.rotate(pygame.image.load("Assets/Classic Board/event.png"), 90)
    chance3 = ChanceBlock(chance3_image, "Chance", 36, chance_card_deck)
    chance3.rect.topleft = (640, 400)
    board.addBlock(chance3)
    #
    block37_image = pygame.transform.rotate(pygame.image.load("Assets/Classic Board/blue.png"), 90)
    block37 = StreetBlock(block37_image, "Block 37", 37, 350, 175, [100, 100, 100, 100, 100], [20, 50, 80, 110, 200, 500], "blue",0)
    block37.rect.topleft = (640, 460)
    board.addBlock(block37)
    #
    super_tax_image = pygame.transform.rotate(pygame.image.load("Assets/Classic Board/event.png"), 90)
    super_tax = LuxuryTaxBlock(super_tax_image, "Super Tax", 38, 100)
    super_tax.rect.topleft = (640, 520)
    board.addBlock(super_tax)
    #
    block39_image = pygame.transform.rotate(pygame.image.load("Assets/Classic Board/blue.png"), 90)
    block39 = StreetBlock(block39_image, "Block 39", 39, 400, 200, [100, 100, 100, 100, 100], [20, 50, 80, 110, 200, 500], "blue",0)
    block39.rect.topleft = (640, 580)
    board.addBlock(block39)
    #
    for block in board.blocks:
        block.generateMask()
    
    
    player_token = [
        PlayerToken(pygame.image.load("Assets/Player/pink.png")), 
        PlayerToken(pygame.image.load("Assets/Player/orange.png")), 
        PlayerToken(pygame.image.load("Assets/Player/green.png")), 
        PlayerToken(pygame.image.load("Assets/Player/blue.png"))
    ]
    market = StockMarket([
        Stock("TSMC", 2000), 
        Stock("Foxconn", 1300), 
        Stock("Delta", 1000)
    ])
    player_icons = [
        PlayerIcon(pygame.transform.scale(pygame.image.load("Assets/TaiwanBoard/PlayerIcons/Birdy.png"), (100, 100)), (235, 105)), 
        PlayerIcon(pygame.transform.scale(pygame.image.load("Assets/TaiwanBoard/PlayerIcons/Birdy.png"), (100, 100)), (335, 105)), 
        PlayerIcon(pygame.transform.scale(pygame.image.load("Assets/TaiwanBoard/PlayerIcons/Birdy.png"), (100, 100)), (435, 105)), 
        PlayerIcon(pygame.transform.scale(pygame.image.load("Assets/TaiwanBoard/PlayerIcons/Birdy.png"), (100, 100)), (535, 105))
    ]
    players = [
        Player("Alice", 0, player_token[0], player_icons[0], StockMarketAccount(market), [Rabbit(), Bomb()], balance = 25000, health_point = 100), 
        Player("Bob", 1, player_token[1], player_icons[1], StockMarketAccount(market), [Turtle(), Pistol()], balance = 25000, health_point = 100), 
        Player("Sean", 2, player_token[2], player_icons[2], StockMarketAccount(market), [Lord(), Barrier()], balance = 25000, health_point = 100), 
        Player("Andrew", 3, player_token[3], player_icons[3], StockMarketAccount(market), [Digger(), Lord()], balance = 25000, health_point = 100)
    ]
    game = Game(
        (1280, 720), 
        board,  
        players, 
        pygame.image.load("Assets/TaiwanBoard/raw/white.png"), 
        market, 
        pygame.image.load("Assets/TaiwanBoard/raw/white.png"), 
        pygame.image.load("Assets/action menu/green.png"), 
        icons, 
        [Pistol, Bomb, Digger, Turtle, Rabbit, Barrier, Lord]
    )
    game.now_player_index = 0
    return game
