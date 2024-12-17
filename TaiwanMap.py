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
        pygame.transform.scale(pygame.image.load("Assets/TaiwanBoard/Props/Pistol.jpg"), (180, 240)), 
        "手槍卡：攻擊選定玩家，造成40點傷害。", 
        need_player_selection = True, 
        player_target_filter = lambda player, board, now_player_index, players: player.index != now_player_index, 
        player_target_maximum = 1, 
        effect = pistol
    )

def Barrier() -> Prop:
    def setBarrier(block, selected_blocks: List[BLOCK], board, now_player, selected_players, players):
        if len(selected_blocks) == 1:
            selected_blocks[0].has_barrier = True
    return Prop(
        "Barrier", 
        pygame.transform.scale(pygame.image.load("Assets/TaiwanBoard/Props/Barrier.jpg"), (180, 240)), 
        "路障卡：在選定的格子放隱形路障，阻擋下一位進入該格的玩家（包括自己）。", 
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
        pygame.transform.scale(pygame.image.load("Assets/TaiwanBoard/Props/Rabbit.jpg"), (180, 240)), 
        "兔子卡：下次骰出來的點數效果變成兩倍", 
        effect = rabbit
    )

def Turtle() -> Prop:
    def turtle(block, selected_blocks: List[BLOCK], board, now_player, selected_players, players):
        now_player.half_steps = True
    return Prop(
        "Trutle", 
        pygame.transform.scale(pygame.image.load("Assets/TaiwanBoard/Props/Turtle.jpg"), (180, 240)), 
        "烏龜卡：下次骰出來的點數效果變成二分之一倍取下高斯", 
        effect = turtle
    )

def Bomb() -> Prop:
    def bomb(block, selected_blocks: List[BLOCK], board, now_player, selected_players, players):
        block.has_bomb = True
    return Prop(
        "Bomb", 
        pygame.transform.scale(pygame.image.load("Assets/TaiwanBoard/Props/Gernade.jpg"), (180, 240)), 
        "炸彈卡：放一顆隱形炸彈，踩到的人會受到80點傷害", 
        effect = bomb
    )

def Lord() -> Prop:
    def lord(block: BLOCK, selected_blocks: List[BLOCK], board: GameBoard, now_player: Player, selected_players: List[Player], players: list[Player]):
        selected_blocks[0].owner = now_player.index
    def filter(block, board, now_player_index, players):
        return isinstance(block, PROPERTY_BLCOK) and block.owner != now_player_index
    return Prop(
        "Lord", 
        pygame.transform.scale(pygame.image.load("Assets/TaiwanBoard/Props/Lord.jpg"), (180, 240)), 
        "地主卡：強制取得一個有產權的格子的所有權", 
        need_block_selection = True, 
        block_target_filter = filter, 
        block_target_maximum = 1, 
        effect = lord
    )

def Digger() -> Prop:
    def digger(block: BLOCK, selected_blocks: List[BLOCK], board: GameBoard, now_player: Player, selected_players: List[Player], players: list[Player]):
        selected_blocks[0].house_amount = 0
    def filter(block, board, now_player_index, players):
        return isinstance(block, StreetBlock) and block.owner != now_player_index and block.owner != None and block.house_amount > 0
    return Prop(
        "Digger", 
        pygame.transform.scale(pygame.image.load("Assets/TaiwanBoard/Props/Digger.jpg"), (180, 240)), 
        "拆房卡：把一個有房子的格子夷平",
        need_block_selection = True, 
        block_target_filter = filter, 
        block_target_maximum = 1, 
        effect = digger
    )

def Reverse() -> Prop:
    def reverse(block: BLOCK, selected_blocks: List[BLOCK], board: GameBoard, now_player: Player, selected_players: List[Player], players: list[Player]):
        now_player.identification = selected_players[0].index
    return Prop(
        "Reverse", 
        pygame.transform.scale(pygame.image.load("Assets/TaiwanBoard/Props/reverse.jpg"), (180, 240)), 
        "嫁禍卡：選一個玩家，這回合如果踩到要付過路費的時候變成他付",
        need_player_selection = True, 
        player_target_filter = lambda player, board, now_player_index, players: player.index != now_player_index, 
        player_target_maximum = 1, 
        effect = reverse
    )

# TODO
def CreditCard() ->Prop:
    pass

def generateGame() -> Game:
    # random event card deck
    random_event_cards = []
    img1 = pygame.image.load("Assets/TaiwanBoard/RandomEvents/三寶.jpg")
    def sanbao(block: BLOCK, selected_blocks: List[BLOCK], board: GameBoard, now_player: Player, selected_players: List[Player], players: list[Player]):
        affected = block.index
        for i in range(5):
            affected = (affected + 1) % len(board.blocks)
            for player in players:
                if player.position == affected:
                    player.stop_round = 2
            now_block = board.blocks[affected]
            now_block.has_barrier = now_block.has_bomb = False
    random_event_cards.append(EventCard(img1, 25, effect=sanbao))
    
    img2 = pygame.image.load("Assets/TaiwanBoard/RandomEvents/愛心筆.jpg")
    def aishinbi(block: BLOCK, selected_blocks: List[BLOCK], board: GameBoard, now_player: Player, selected_players: List[Player], players: list[Player]):
        now_player.balance -= 1500
    random_event_cards.append(EventCard(img2, 25, effect=aishinbi))

    
    img3 = pygame.image.load("Assets/TaiwanBoard/RandomEvents/慢速婆婆.jpg")
    def mansupopo(block: BLOCK, selected_blocks: List[BLOCK], board: GameBoard, now_player: Player, selected_players: List[Player], players: list[Player]):
        now_player.balance -= 3000
    random_event_cards.append(EventCard(img3, 25, effect=mansupopo))


    img4 = pygame.image.load("Assets/TaiwanBoard/RandomEvents/野狗.jpg")
    def cuteDog(block: BLOCK, selected_blocks: List[BLOCK], board: GameBoard, now_player: Player, selected_players: List[Player], players: list[Player]):
        now_player.decreaseHealthPoint(50)
    random_event_cards.append(EventCard(img4, 25, effect=cuteDog))

    random_event_card_deck = EventCardDeck(random_event_cards)


    # chance card deck
    chance_card_deck_list = []

    # 一百塊
    image_1 = pygame.transform.scale(pygame.image.load("Assets/EventCards/Chance/一百塊 勒.jpg"), (400, 580))
    def addOneHundred(block: BLOCK, selected_blocks: List[BLOCK], board: GameBoard, now_player: Player, selected_players: List[Player], players: list[Player]):
        now_player.balance += 100
    chance_card_deck_list.append(EventCard(image_1, 10, effect=addOneHundred))

    # 小新的車車
    image_2 = pygame.transform.scale(pygame.image.load("Assets/EventCards/Chance/小新的車車.jpg"), (400, 580))
    def aCar(block: BLOCK, selected_blocks: List[BLOCK], board: GameBoard, now_player: Player, selected_players: List[Player], players: list[Player]):
        if len(now_player.props) <= 4:
            now_player.props.append(Rabbit())
    chance_card_deck_list.append(EventCard(image_2, 10, effect=aCar))

    # 出事了阿北
    image_3 = pygame.transform.scale(pygame.image.load("Assets/EventCards/Chance/出事了阿北.jpg"), (400, 580))
    def kP(block: BLOCK, selected_blocks: List[BLOCK], board: GameBoard, now_player: Player, selected_players: List[Player], players: list[Player]):
        now_player.position = now_player.token_position = board.prison_block_index
        now_block = board.blocks[board.prison_block_index]
        now_player.stop_round = 3
        now_player.token.rect.topleft = addCoordinates(now_block.rect.center, TOKEN_OFFSET[now_player.index])
    chance_card_deck_list.append(EventCard(image_3, 5, effect=kP))

    # 外星人
    image_4 = pygame.transform.scale(pygame.image.load("Assets/EventCards/Chance/外星人.jpg"), (400, 580))
    def aliens(block: BLOCK, selected_blocks: List[BLOCK], board: GameBoard, now_player: Player, selected_players: List[Player], players: list[Player]):
        now_player.stop_round = 1
    chance_card_deck_list.append(EventCard(image_4, 10, effect=aliens))

    # 快不行了
    image_5 = pygame.transform.scale(pygame.image.load("Assets/EventCards/Chance/快不行了.jpg"), (400, 580))
    def scldIsNightmare(block: BLOCK, selected_blocks: List[BLOCK], board: GameBoard, now_player: Player, selected_players: List[Player], players: list[Player]):
        now_player.balance -= 1000
    chance_card_deck_list.append(EventCard(image_5, 10, effect=scldIsNightmare))

    # 穿牆術
    image_6 = pygame.transform.scale(pygame.image.load("Assets/EventCards/Chance/穿牆術.jpg"), (400, 580))
    def passWall(block: BLOCK, selected_blocks: List[BLOCK], board: GameBoard, now_player: Player, selected_players: List[Player], players: list[Player]):
        now_player.invisible_round = True
    chance_card_deck_list.append(EventCard(image_6, 10, effect=passWall))

    # 野豬騎士
    image_7 = pygame.transform.scale(pygame.image.load("Assets/EventCards/Chance/野豬騎士.jpg"), (400, 580))
    def hogRider(block: BLOCK, selected_blocks: List[BLOCK], board: GameBoard, now_player: Player, selected_players: List[Player], players: list[Player]):
        selected_blocks[0].owner = now_player.index
    def hogRiderBlockTargetFilter(block, board, now_player_index, players):
        return isinstance(block, BLOCK) and block.owner != now_player_index
    chance_card_deck_list.append(EventCard(image_7, 2, need_block_selection=True, block_target_filter = hogRiderBlockTargetFilter, block_target_maxmium=1, effect=hogRider))

    # 撿到錢包
    image_8 = pygame.transform.scale(pygame.image.load("Assets/EventCards/Chance/撿到錢包.jpg"), (400, 580))
    def aWallet(block: BLOCK, selected_blocks: List[BLOCK], board: GameBoard, now_player: Player, selected_players: List[Player], players: list[Player]):
        now_player.balance += 1000
    chance_card_deck_list.append(EventCard(image_8, 10, effect=aWallet))

    # 幫幫人民的啦
    image_9 = pygame.transform.scale(pygame.image.load("Assets/EventCards/Chance/幫幫人民的啦.jpg"), (400, 580))
    def giveMoney(block: BLOCK, selected_blocks: List[BLOCK], board: GameBoard, now_player: Player, selected_players: List[Player], players: list[Player]):
        now_player.balance -= 1000
    chance_card_deck_list.append(EventCard(image_9, 10, effect=giveMoney))

    # chill guy
    image_10 = pygame.transform.scale(pygame.image.load("Assets/EventCards/chance/chill guy.jpg"), (400, 580))
    def chillGuy(block: BLOCK, selected_blocks: List[BLOCK], board: GameBoard, now_player: Player, selected_players: List[Player], players: list[Player]):
        now_player.stop_round = 1
    chance_card_deck_list.append(EventCard(image_10, 10, effect=chillGuy))

    # Community Chest Deck
    community_chest_deck_list = []

    # 大爆炸
    image_11 = pygame.transform.scale(pygame.image.load("Assets/EventCards/CommunityChest/大爆炸.jpg"), (400, 580))
    def explosion(block: BLOCK, selected_blocks: List[BLOCK], board: GameBoard, now_player: Player, selected_players: List[Player], players: list[Player]):
        for blk in board.blocks:
            blk.house_amount = 0
    community_chest_deck_list.append(EventCard(image_11, 3, effect=explosion))

    # 月光刑警
    image_12 = pygame.transform.scale(pygame.image.load("Assets/EventCards/CommunityChest/月光刑警.jpg"), (400, 580))
    def moonlightPower(block: BLOCK, selected_blocks: List[BLOCK], board: GameBoard, now_player: Player, selected_players: List[Player], players: list[Player]):
        now_player.token_position = now_player.position = selected_blocks[0].index
        now_block = board.blocks[board.prison_block_index]
        now_player.token.rect.topleft = addCoordinates(now_block.rect.center, TOKEN_OFFSET[now_player.index])
    def moonlightPowerBlockTargetFilter(block, board, now_player_index, players):
        return True
    community_chest_deck_list.append(EventCard(image_12, 10, need_block_selection=True, block_target_filter=moonlightPowerBlockTargetFilter, block_target_maxmium=1 , effect=moonlightPower))

    # 出車禍
    image_13 = pygame.transform.scale(pygame.image.load("Assets/EventCards/CommunityChest/出車禍.jpg"), (400, 580))
    def michael(block: BLOCK, selected_blocks: List[BLOCK], board: GameBoard, now_player: Player, selected_players: List[Player], players: list[Player]):
        now_player.stop_round = 2
    community_chest_deck_list.append(EventCard(image_13, 20, effect=michael))

    # 好友基德
    image_14 = pygame.transform.scale(pygame.image.load("Assets/EventCards/CommunityChest/好友基德.jpg"), (400, 580))
    def goodFreind(block: BLOCK, selected_blocks: List[BLOCK], board: GameBoard, now_player: Player, selected_players: List[Player], players: list[Player]):
        now_player.balance += randint(7000, 15000)
    community_chest_deck_list.append(EventCard(image_14, 20, effect=goodFreind))

    # 凍蒜
    image_15 = pygame.transform.scale(pygame.image.load("Assets/EventCards/CommunityChest/凍蒜.jpg"), (400, 580))
    def tiKoLiang(block: BLOCK, selected_blocks: List[BLOCK], board: GameBoard, now_player: Player, selected_players: List[Player], players: list[Player]):
        now_player.balance += randint(7000, 15000)
    community_chest_deck_list.append(EventCard(image_15, 20, effect=tiKoLiang))

    # 跌價妖怪女
    image_16 = pygame.transform.scale(pygame.image.load("Assets/EventCards/CommunityChest/跌價妖怪女.jpg"), (400, 580))
    def Ume(block: BLOCK, selected_blocks: List[BLOCK], board: GameBoard, now_player: Player, selected_players: List[Player], players: list[Player]):
        now_player.balance >>= 1
    community_chest_deck_list.append(EventCard(image_16, 20, effect=Ume))

    # 檢舉達人
    image_17 = pygame.transform.scale(pygame.image.load("Assets/EventCards/CommunityChest/檢舉達人.jpg"), (400, 580))
    def reporter(block: BLOCK, selected_blocks: List[BLOCK], board: GameBoard, now_player: Player, selected_players: List[Player], players: list[Player]):
        now_player.position = now_player.token_position = board.prison_block_index
        now_block = board.blocks[board.prison_block_index]
        now_player.stop_round = 3
        now_player.token.rect.topleft = addCoordinates(now_block.rect.center, TOKEN_OFFSET[now_player.index])
    community_chest_deck_list.append(EventCard(image_17, 10, need_player_selection=True, player_target_filter= lambda player, board, now_player_index, players: player.index != now_player_index,player_target_maximum=1 , effect=reporter))

    # 魔法小卡
    image_18 = pygame.transform.scale(pygame.image.load("Assets/EventCards/CommunityChest/魔法小卡.jpg"), (400, 580))
    def creditCard(block: BLOCK, selected_blocks: List[BLOCK], board: GameBoard, now_player: Player, selected_players: List[Player], players: list[Player]):
        now_player.props.append(CreditCard())
    # community_chest_deck_list.append(EventCard(image_18, 3, effect=creditCard))

    # gg
    image_19 = pygame.transform.scale(pygame.image.load("Assets/EventCards/CommunityChest/gg.jpg"), (400, 580))
    def goodGame(block: BLOCK, selected_blocks: List[BLOCK], board: GameBoard, now_player: Player, selected_players: List[Player], players: list[Player]):
        for blk in board.blocks:
            if isinstance(blk, PROPERTY_BLCOK) and blk.owner == now_player.index:
                blk.owner = None
                blk.house_amount = 0
        now_player.balance = 25000
        now_player.props.clear()
    community_chest_deck_list.append(EventCard(image_19, 2, effect=goodGame))

    chance_card_deck = EventCardDeck(chance_card_deck_list)
    community_chest_deck = EventCardDeck(community_chest_deck_list)

    ## 

    board = GameBoard()
    icons = []
    #####
    go_image = pygame.image.load("Assets/TaiwanBoard/Blocks/start.png")
    go = StartBlock(pygame.transform.scale(go_image, (80, 80)), "Go", 0, 2000)
    go.rect.topleft = (640, 640)
    icons.append(pygame.transform.scale(go_image, (300, 300)))
    board.addBlock(go)
    #
    keelung_image = pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/Keelung.jpg"), -90)
    keelung = StreetBlock(pygame.transform.scale(keelung_image, (60, 80)), "Keelung", 1, 2000, 30, [2400, 2400, 2400, 2400, 2400], [500 + i * 600 for i in range(6)], "red", 0)
    keelung.rect.topleft = (580,640)
    icons.append(pygame.transform.scale(keelung_image, (300, 400)))
    board.addBlock(keelung)
    #
    commuity_chest1_image = pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/CommunityChest.jpg"), -90)
    commuity_chest1 = CommunityChestBlock(pygame.transform.scale(commuity_chest1_image, (60, 80)), "CommunityChest", 2, community_chest_deck)
    commuity_chest1.rect.topleft = (520, 640)
    icons.append(pygame.transform.scale(commuity_chest1_image, (300, 400)))
    board.addBlock(commuity_chest1)
    #
    guishan_island_image = pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/GuishanIsland.jpg"), -90)
    guishan_island = StreetBlock(pygame.transform.scale(guishan_island_image, (60, 80)), "Guishan Island", 3, 2100, 30, [2400, 2400, 2400, 2400, 2400], [525 + i * 600 for i in range(6)], "red",0)
    guishan_island.rect.topleft = (460,640)
    icons.append(pygame.transform.scale(guishan_island_image, (300, 400)))
    board.addBlock(guishan_island)
    #####
    income_tax_image = pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/Taxation.jpg"), -90)
    income_tax = IncomeTaxBlock(pygame.transform.scale(income_tax_image, (60, 80)), "Tax", 4, 1000)
    income_tax.rect.topleft = (400, 640)
    icons.append(pygame.transform.scale(income_tax_image, (300, 400)))
    board.addBlock(income_tax)
    #####
    station1_image = pygame.image.load("Assets/TaiwanBoard/Blocks/Railroad1.png")
    station1 = RailroadBlock(pygame.transform.scale(station1_image, (60, 80)), "Station 1", 5, 1500, 100, [500, 1500, 3000, 6000])
    station1.rect.topleft = (340, 640)
    icons.append(pygame.transform.scale(station1_image, (300, 400)))
    board.addBlock(station1)
    #
    yilan_image = pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/Yilan.jpg"), -90)
    yilan = StreetBlock(pygame.transform.scale(yilan_image, (60, 80)), "Yilan", 6, 2400, 30, [2400, 2400, 2400, 2400, 2400], [600 + i * 600 for i in range(6)], "red",0)
    yilan.rect.topleft = (280,640)
    icons.append(pygame.transform.scale(yilan_image, (300, 400)))
    board.addBlock(yilan)
    #
    chance1_image = pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/Chance.jpg"), -90)
    chance1 = ChanceBlock(pygame.transform.scale(chance1_image, (60, 80)), "Chance", 7, chance_card_deck)
    chance1.rect.topleft = (220, 640)
    icons.append(pygame.transform.scale(chance1_image, (300, 400)))
    board.addBlock(chance1)
    #
    hualien_image = pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/Hualien.jpg"), -90)
    hualien = StreetBlock(pygame.transform.scale(hualien_image, (60, 80)), "Hualien", 8, 2800, 30, [2400, 2400, 2400, 2400, 2400], [700 + i * 600 for i in range(6)], "red",0)
    hualien.rect.topleft = (160,640)
    icons.append(pygame.transform.scale(hualien_image, (300, 400)))
    board.addBlock(hualien)
    #
    taitung_image = pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/Taitung.jpg"), -90)
    taitung = StreetBlock(pygame.transform.scale(taitung_image, (60, 80)), "Taitung", 9, 2600, 30, [2400, 2400, 2400, 2400, 2400], [650 + i * 600 for i in range(6)], "red",0)
    taitung.rect.topleft = (100,640)
    icons.append(pygame.transform.scale(taitung_image, (300, 400)))
    board.addBlock(taitung)
    #####
    in_jail_or_just_visit_image = pygame.image.load("Assets/TaiwanBoard/Blocks/jail.png")
    in_jail_or_just_visit = InJailOrJustVisitingBlock(pygame.transform.scale(in_jail_or_just_visit_image, (80, 80)), "Jail", 10)
    in_jail_or_just_visit.rect.topleft = (20, 640)
    icons.append(pygame.transform.scale(in_jail_or_just_visit_image, (300, 300)))
    board.addBlock(in_jail_or_just_visit)
    #
    orchidisland_image = pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/OrchidIsland.jpg"), 180)
    orchidisland = StreetBlock(pygame.transform.scale(orchidisland_image, (80, 60)), "Orchid Island", 11, 2400, 70, [2400, 2400, 2400, 2400, 2400], [600 + i * 600 for i in range(6)], "purple",0)
    orchidisland.rect.topleft = (20, 580)
    icons.append(pygame.transform.scale(pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/OrchidIsland.jpg"), -90), (300, 400)))
    board.addBlock(orchidisland)
    #
    utility1_image = pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/ElectricCompany.jpg"), 180)
    utility1 = UtilityBlock(pygame.transform.scale(utility1_image, (80, 60)), "Electric Company", 12, 1500, 75, [1000, 3000])
    utility1.rect.topleft = (20, 520)
    icons.append(pygame.transform.scale(pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/ElectricCompany.jpg"), -90), (300, 400)))
    board.addBlock(utility1)
    #
    pingtung_image = pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/Pingtung.jpg"), 180)
    pingtung = StreetBlock(pygame.transform.scale(pingtung_image, (80, 60)), "Pingtung", 13, 2800, 70, [2400, 2400, 2400, 2400, 2400], [700 + i * 600 for i in range(6)], "purple",0)
    pingtung.rect.topleft = (20, 460)
    icons.append(pygame.transform.scale(pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/Pingtung.jpg"), -90), (300, 400)))
    board.addBlock(pingtung)
    #
    kaohsiung_image = pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/Kaohsiung.jpg"), 180)
    kaohsiung = StreetBlock(pygame.transform.scale(kaohsiung_image, (80, 60)), "Kaohsiung", 14, 3400, 80, [2400, 2400, 2400, 2400, 2400], [850 + i * 600 for i in range(6)], "purple",0)
    kaohsiung.rect.topleft = (20, 400)
    icons.append(pygame.transform.scale(pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/Kaohsiung.jpg"), -90), (300, 400)))
    board.addBlock(kaohsiung)
    #####
    station2_image = pygame.image.load("Assets/TaiwanBoard/Blocks/Railroad2.png")
    station2 = RailroadBlock(pygame.transform.scale(pygame.transform.rotate(station2_image, 270), (80, 60)), "Station 2", 15, 1500, 100, [500, 1500, 3000, 6000])
    station2.rect.topleft = (20, 340)
    icons.append(pygame.transform.scale(station2_image, (300, 400)))
    board.addBlock(station2)
    #
    bakery1_image = pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/BakeryShop.png"), 270)
    bakery1 = BreadStoreBlock(pygame.transform.scale(bakery1_image, (80, 60)), "BakeryShop", 16, 5000, 90, [], None, 0)
    bakery1.rect.topleft = (20, 280)
    icons.append(pygame.transform.scale(pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/BakeryShop.png"), 0), (300, 400)))
    board.addBlock(bakery1)
    #
    commuity_chest2_image = pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/CommunityChest.jpg"), 180)
    commuity_chest2 = CommunityChestBlock(pygame.transform.scale(commuity_chest2_image, (80, 60)), "CommunityChest", 17, community_chest_deck)
    commuity_chest2.rect.topleft = (20, 220)
    icons.append(pygame.transform.scale(pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/CommunityChest.jpg"), -90), (300, 400)))
    board.addBlock(commuity_chest2)
    #
    tainan_image = pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/Tainan.jpg"), 180)
    tainan = StreetBlock(pygame.transform.scale(tainan_image, (80, 60)), "Tainan", 18, 3300, 80, [2400, 2400, 2400, 2400, 2400], [825 + i * 600 for i in range(6)], "purple",0)
    tainan.rect.topleft = (20, 160)
    icons.append(pygame.transform.scale(pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/Tainan.jpg"), -90), (300, 400)))
    board.addBlock(tainan)
    #
    prop1_image = pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/PropBlock.jpg"), 180)
    prop1 = PropBlcok(pygame.transform.scale(prop1_image, (80, 60)), "PropBlock", 19)
    prop1.rect.topleft = (20, 100)
    icons.append(pygame.transform.scale(pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/PropBlock.jpg"), -90), (300, 400)))
    board.addBlock(prop1)
    #
    harbor_image = pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/Harbor.png"), 0)
    harbor = HarborBlock(pygame.transform.scale(harbor_image, (80, 80)), "Harbor", 20, True)
    harbor.rect.topleft = (20, 20)
    icons.append(pygame.transform.scale(pygame.image.load("Assets/TaiwanBoard/Blocks/Harbor.png"), (300, 300)))
    board.addBlock(harbor)
    #
    chiayi_image = pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/Chiayi.jpg"), 90)
    chiayi = StreetBlock(pygame.transform.scale(chiayi_image, (60, 80)), "Chiayi", 21, 2800, 80, [2400, 2400, 2400, 2400, 2400], [700 + i * 600 for i in range(6)], "purple",0)
    chiayi.rect.topleft = (100, 20)
    icons.append(pygame.transform.scale(pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/Chiayi.jpg"), -90), (300, 400)))
    board.addBlock(chiayi)
    #
    chance2_image = pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/Chance.jpg"), 90)
    chance2 = ChanceBlock(pygame.transform.scale(chance2_image, (60, 80)), "Chance", 22, chance_card_deck)
    chance2.rect.topleft = (160, 20)
    icons.append(pygame.transform.scale(pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/Chance.jpg"), -90), (300, 400)))
    board.addBlock(chance2)
    #
    sunmoonlake_image = pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/SunMoonLake.jpg"), 90)
    sunmoonlake = StreetBlock(pygame.transform.scale(sunmoonlake_image, (60, 80)), "Sun Moon Lake", 23, 3400, 80, [2400, 2400, 2400, 2400, 2400], [850 + i * 600 for i in range(6)], "purple",0)
    sunmoonlake.rect.topleft = (220, 20)
    icons.append(pygame.transform.scale(pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/SunMoonLake.jpg"), -90), (300, 400)))
    board.addBlock(sunmoonlake)
    #
    bakery2_image = pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/BakeryShop.png"), 180)
    bakery2 = BreadStoreBlock(pygame.transform.scale(bakery2_image, (60, 80)), "BakeryShop", 24, 5000, 90, [0], None, 0)
    bakery2.rect.topleft = (280, 20)
    icons.append(pygame.transform.scale(pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/BakeryShop.png"), 0), (300, 400)))
    board.addBlock(bakery2)
    #####
    station3_image = pygame.image.load("Assets/TaiwanBoard/Blocks/Railroad3.png")
    station3 = RailroadBlock(pygame.transform.scale(pygame.transform.rotate(station3_image, 180), (60, 80)), "Station 3", 25, 1500, 100, [500, 1500, 3000, 6000])
    station3.rect.topleft = (340, 20)
    icons.append(pygame.transform.scale(station3_image, (300, 400)))
    board.addBlock(station3)
    #
    prop2_image = pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/PropBlock.jpg"), 90)
    prop2 = PropBlcok(pygame.transform.scale(prop2_image, (60, 80)), "PropBlock", 26)
    prop2.rect.topleft = (400, 20)
    icons.append(pygame.transform.scale(pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/PropBlock.jpg"), -90), (300, 400)))
    board.addBlock(prop2)
    #
    taichung_image = pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/Taichung.jpg"), 90)
    taichung = StreetBlock(pygame.transform.scale(taichung_image, (60, 80)), "Taichung", 27, 3600, 80, [2400, 2400, 2400, 2400, 2400], [900 + i * 600 for i in range(6)], "purple",0)
    taichung.rect.topleft = (460, 20)
    icons.append(pygame.transform.scale(pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/Taichung.jpg"), -90), (300, 400)))
    board.addBlock(taichung)
    #
    utility2_image = pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/ElectricCompany.jpg"), 90)
    utility2 = UtilityBlock(pygame.transform.scale(utility2_image, (60, 80)), "Electric Company", 28, 1500, 75, [1000, 3000])
    utility2.rect.topleft = (520, 20)
    icons.append(pygame.transform.scale(pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/ElectricCompany.jpg"), -90), (300, 400)))
    board.addBlock(utility2)
    #
    miaoli_image = pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/Miaoli.jpg"), 90)
    miaoli = StreetBlock(pygame.transform.scale(miaoli_image, (60, 80)), "Miaoli", 29, 2800, 80, [2400, 2400, 2400, 2400, 2400], [700 + i * 600 for i in range(6)], "purple",0)
    miaoli.rect.topleft = (580, 20)
    icons.append(pygame.transform.scale(pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/Miaoli.jpg"), -90), (300, 400)))
    board.addBlock(miaoli)
    #
    airport_image = pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/Airport.jpg"), 0)
    airport = AirportBlock(pygame.transform.scale(airport_image, (80, 80)), "Airport", 30, True)
    airport.rect.topleft = (640, 20)
    icons.append(pygame.transform.scale(pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/Airport.jpg"), 0), (300, 300)))
    board.addBlock(airport)
    #
    hsinchu_image = pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/Hsinchu.jpg"), 0)
    hsinchu = StreetBlock(pygame.transform.scale(hsinchu_image, (80, 60)), "Hsinchu", 31, 3100, 80, [2400, 2400, 2400, 2400, 2400], [775 + i * 600 for i in range(6)], "purple",0)
    hsinchu.rect.topleft = (640, 100)
    icons.append(pygame.transform.scale(pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/Hsinchu.jpg"), -90), (300, 400)))
    board.addBlock(hsinchu)
    #
    newtaipei_image = pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/NewTaipeiCity.jpg"), 0)
    newtaipei = StreetBlock(pygame.transform.scale(newtaipei_image, (80, 60)), "New Taipei City", 32, 3800, 80, [2400, 2400, 2400, 2400, 2400], [950 + i * 600 for i in range(6)], "purple",0)
    newtaipei.rect.topleft = (640, 160)
    icons.append(pygame.transform.scale(pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/NewTaipeiCity.jpg"), -90), (300, 400)))
    board.addBlock(newtaipei)
    #
    commuity_chest3_image = pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/CommunityChest.jpg"), 0)
    commuity_chest3 = CommunityChestBlock(pygame.transform.scale(commuity_chest3_image, (80, 60)), "CommunityChest", 33, community_chest_deck)
    commuity_chest3.rect.topleft = (640, 220)
    icons.append(pygame.transform.scale(pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/CommunityChest.jpg"), -90), (300, 400)))
    board.addBlock(commuity_chest3)
    #
    taipei_image = pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/Taipei.jpg"), 0)
    taipei = StreetBlock(pygame.transform.scale(taipei_image, (80, 60)), "Taipei", 34, 4000, 80, [2400, 2400, 2400, 2400, 2400], [1000 + i * 600 for i in range(6)], "purple",0)
    taipei.rect.topleft = (640, 280)
    icons.append(pygame.transform.scale(pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/Taipei.jpg"), -90), (300, 400)))
    board.addBlock(taipei)
    #####
    station4_image = pygame.image.load("Assets/TaiwanBoard/Blocks/Railroad4.png")
    station4 = RailroadBlock(pygame.transform.scale(pygame.transform.rotate(station4_image, 90), (80, 60)), "Station 4", 35, 1500, 100, [500, 1500, 3000, 6000])
    station4.rect.topleft = (640, 340)
    icons.append(pygame.transform.scale(station4_image, (300, 400)))
    board.addBlock(station4)
    #
    chance3_image = pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/Chance.jpg"), 0)
    chance3 = ChanceBlock(pygame.transform.scale(chance3_image, (80, 60)), "Chance", 36, chance_card_deck)
    chance3.rect.topleft = (640, 400)
    icons.append(pygame.transform.scale(pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/Chance.jpg"), -90), (300, 400)))
    board.addBlock(chance3)
    #
    ntu_image = pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/NTU.jpg"), 0)
    ntu = StreetBlock(pygame.transform.scale(ntu_image, (80, 60)), "NTU", 37, 5600, 80, [2400, 2400, 2400, 2400, 2400], [1600 + i * 600 for i in range(6)], "purple",0)
    ntu.rect.topleft = (640, 460)
    icons.append(pygame.transform.scale(pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/NTU.jpg"), -90), (300, 400)))
    board.addBlock(ntu)
    #
    income_tax1_image = pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/Taxation.jpg"), 0)
    income_tax1 = IncomeTaxBlock(pygame.transform.scale(income_tax1_image, (80, 60)), "Tax", 38, 1500)
    income_tax1.rect.topleft = (640, 520)
    icons.append(pygame.transform.scale(pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/Taxation.jpg"), -90), (300, 400)))
    board.addBlock(income_tax1)
    #
    renovation_image = pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/RenovationCompany.jpg"), 0)
    renovation = RenovationCompanyBlcok(pygame.transform.scale(renovation_image, (80, 60)), "Decoration Company", 39, True)
    renovation.rect.topleft = (640, 580)
    icons.append(pygame.transform.scale(pygame.transform.rotate(pygame.image.load("Assets/TaiwanBoard/Blocks/RenovationCompany.jpg"), -90), (300, 400)))
    board.addBlock(renovation)
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
        PlayerIcon(pygame.transform.scale(pygame.image.load("Assets/TaiwanBoard/PlayerIcons/catty.jpg"), (100, 100)), (235, 105)), 
        PlayerIcon(pygame.transform.scale(pygame.image.load("Assets/TaiwanBoard/PlayerIcons/kitten.jpg"), (100, 100)), (335, 105)), 
        PlayerIcon(pygame.transform.scale(pygame.image.load("Assets/TaiwanBoard/PlayerIcons/chidaomimmaomao.jpg"), (100, 100)), (435, 105)), 
        PlayerIcon(pygame.transform.scale(pygame.image.load("Assets/TaiwanBoard/PlayerIcons/pop.jpg"), (100, 100)), (535, 105))
    ]
    players = [
        Player("pink", 0, player_token[0], player_icons[0], StockMarketAccount(market), [Barrier(), Barrier(), Barrier(), Barrier()], balance = 25000, health_point = 100), 
        Player("orange", 1, player_token[1], player_icons[1], StockMarketAccount(market), [Rabbit(), Turtle()], balance = 25000, health_point = 100), 
        Player("green", 2, player_token[2], player_icons[2], StockMarketAccount(market), [Rabbit(), Turtle()], balance = 25000, health_point = 100), 
        Player("blue", 3, player_token[3], player_icons[3], StockMarketAccount(market), [Rabbit(), Turtle()], balance = 25000, health_point = 100)
    ]
    game = Game(
        (1280, 720), 
        board,  
        players, 
        pygame.image.load("Assets/TaiwanBoard/raw/white.png"), 
        market, 
        pygame.image.load("Assets/TaiwanBoard/raw/white.png"), 
        pygame.image.load("Assets/TaiwanBoard/raw/white.png"), 
        icons, 
        [Pistol, Bomb, Digger, Turtle, Rabbit, Barrier, Lord, Reverse], 
        random_event_card_deck        
    )
    game.now_player_index = 0
    return game
