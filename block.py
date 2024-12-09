import pygame
from typing import List, Union

class BlockType:
    # properties
    STREET = 1
    RAILROAD = 2
    UTILITY = 3
    PROPERTIES = (1, 2, 3)
    # event
    CHANCE = 4
    COMMUNITY_CHEST = 5
    EVENT = (4, 5)
    # tax
    LUXURY_TAX = 6
    INCOME_TAX = 7
    TAX = (6, 7)
    # corners
    START = 8
    IN_JAIL_OR_JUST_VISITING = 9
    FREE_PARKING = 10
    IMPRISON = 11
    CORNER = (8, 9, 10, 11)
    
class BlockStatus:
    # basic (2 bit)
    ENABLED = 0b0001
    SELECTED = 0b0010
    # properties (2 bit)
    OWNED = 0b0100


class Block:
    def __init__(self, image: pygame.Surface, name, type, index, status):
        self.name = name
        self.type = type
        self.index = index
        self.status = status
        # 
        self.image = image
        self.rect = self.image.get_rect()
    def generateMask(self):
        self.disabled_mask = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        self.disabled_mask.fill((0, 0, 0, 100))
        self.disabled_mask_rect = self.disabled_mask.get_rect()
        self.disabled_mask_rect.topleft = self.rect.topleft
        self.selected_mask = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        self.selected_mask.fill((255, 255, 0, 100))
        self.selected_mask_rect = self.selected_mask.get_rect()
        self.selected_mask_rect.topleft = self.rect.topleft
        #
        self.owner_masks = [pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA) for _ in range(4)]
        self.owner_masks[0].fill((255, 0, 0, 50))
        self.owner_masks[1].fill((255, 255, 0, 50))
        self.owner_masks[2].fill((0, 255, 0, 50))
        self.owner_masks[3].fill((0, 0, 255, 50))
        self.owner_mask_rects = [mask.get_rect() for mask in self.owner_masks]
        for rect in self.owner_mask_rects:
            rect.topleft= self.rect.topleft

class PropertyBlock(Block):
    def __init__(self, image: pygame.Surface, name, type, index, purchase_price, mortagate_price, rent_chart, owner, status):
        super().__init__(image, name, type, index, status)
        self.owner = owner
        # monetary variables
        self.purchase_price = purchase_price
        self.mortagate_price = mortagate_price
        self.rent_chart = rent_chart

class StreetBlock(PropertyBlock):
    def __init__(self, image: pygame.Surface, name, index, purchase_price, mortagate_price, house_price_chart, rent_chart, color_group, house_amount, owner = None, status = BlockStatus.ENABLED):
        super().__init__(image, name, BlockType.STREET, index, purchase_price, mortagate_price, rent_chart, owner, status)
        self.color_group = color_group
        self.house_price_chart = house_price_chart
        self.house_amount = house_amount

class RailroadBlock(PropertyBlock):
    def __init__(self, image: pygame.Surface, name, index, purchase_price, mortagate_price, rent_chart, owner = None, status = BlockStatus.ENABLED):
        super().__init__(image, name, BlockType.RAILROAD, index, purchase_price, mortagate_price, rent_chart, owner, status)

class UtilityBlock(PropertyBlock):
    def __init__(self, image: pygame.Surface, name, index, purchase_price, mortagate_price, rent_chart, owner = None, status = BlockStatus.ENABLED):
        super().__init__(image, name, BlockType.UTILITY, index, purchase_price, mortagate_price, rent_chart, owner, status)

class EventBlock(Block):
    def __init__(self, image: pygame.Surface, name, type, index, deck, status):
        super().__init__(image, name, type, index, status)
        self.deck = deck

class ChanceBlock(EventBlock):
    def __init__(self, image: pygame.Surface, name, index, chance_card_deck, status = BlockStatus.ENABLED):
        super().__init__(image, name, BlockType.CHANCE, index, chance_card_deck, status)

class CommunityChestBlock(EventBlock):
    def __init__(self, image: pygame.Surface, name, index, community_chest_deck, status = BlockStatus.ENABLED):
        super().__init__(image, name, BlockType.COMMUNITY_CHEST, index, community_chest_deck, status)

class TaxBlock(Block):
    def __init__(self, image: pygame.Surface, name, type, index, tax, status):
        super().__init__(image, name, type, index, status)
        self.tax = tax

class LuxuryTaxBlock(TaxBlock):
    def __init__(self, image: pygame.Surface, name, index, luxury_tax, status = BlockStatus.ENABLED):
        super().__init__(image, name, BlockType.LUXURY_TAX, index, luxury_tax, status)

class IncomeTaxBlock(TaxBlock):
    def __init__(self, image: pygame.Surface, name, index, income_tax, status = BlockStatus.ENABLED):
        super().__init__(image, name, BlockType.INCOME_TAX, index, income_tax, status)

class StartBlock(Block):
    def __init__(self, image: pygame.Surface, name, index, salary, status = BlockStatus.ENABLED):
        super().__init__(image, name, BlockType.START, index, status)
        self.salary = salary

class InJailOrJustVisitingBlock(Block):
    def __init__(self, image: pygame.Surface, name, index, status = BlockStatus.ENABLED):
        super().__init__(image, name, BlockType.IN_JAIL_OR_JUST_VISITING, index, status)

class FreeParkingBlock(Block):
    def __init__(self, image: pygame.Surface, name, index, jackpot, status = BlockStatus.ENABLED):
        super().__init__(image, name, BlockType.FREE_PARKING, index, status)
        self.jackpot = jackpot

class ImprisonBlock(Block):
    def __init__(self, image: pygame.Surface, name, index, status = BlockStatus.ENABLED):
        super().__init__(image, name, BlockType.IMPRISON, index, status)

