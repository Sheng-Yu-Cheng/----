from block import *
from constant import *
from typing import Union, List, Tuple
import pygame

class GameBoard:
    def __init__(self):
        self.blocks : List[BLOCK] = []
    def addBlock(self, block: BLOCK):
        self.blocks.append(block)
    def renderToScreen(self, screen: pygame.Surface):
        for block in self.blocks:
            screen.blit(block.image, block.rect)
            if isinstance(block, PROPERTY_BLCOK):
                if (owner := block.owner) != None:
                    screen.blit(block.owner_masks[owner], block.owner_mask_rects[owner])
            if not block.status & BlockStatus.ENABLED:
                screen.blit(block.disabled_mask, block.disabled_mask_rect)
            elif block.status & BlockStatus.SELECTED:
                screen.blit(block.selected_mask, block.selected_mask_rect)


def generateClassicGameBoard() -> GameBoard:
    board = GameBoard()
    #
    go_image = pygame.image.load("Assets/Classic Board/corner.png")
    go = StartBlock(go_image, "Go", 0, 200)
    go.rect.topleft = (640, 640)
    board.addBlock(go)
    #
    block1_image = pygame.image.load("Assets/Classic Board/red.png")
    block1 = StreetBlock(block1_image, "Block 2", 1, 60, 30, [100, 100, 100, 100, 100], [20, 50, 80, 110, 200, 500], "red",0)
    block1.rect.topleft = (580,640)
    board.addBlock(block1)
    #
    commuity_chest1_image = pygame.image.load("Assets/Classic Board/event.png")
    commuity_chest1 = CommunityChestBlock(commuity_chest1_image, "Commmunity Chest", 2, [])
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
    chance1 = ChanceBlock(chance1_image, "Chance", 7, [])
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
    commuity_chest2 = CommunityChestBlock(commuity_chest2_image, "Commmunity Chest", 17, [])
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
    chance2 = ChanceBlock(chance2_image, "Chance", 22, [])
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
    commuity_chest3 = CommunityChestBlock(commuity_chest3_image, "Commmunity Chest", 33, [])
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
    chance3 = ChanceBlock(chance3_image, "Chance", 36, [])
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
    return board