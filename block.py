class BlockType:
    # properties
    STREET = 1
    RAILROAD = 2
    UTILITY = 3
    # event
    CHANCE = 4
    COMMUNITY_CHEST = 5
    # tax
    LUXURY_TAX = 6
    INCOME_TAX = 7
    # corners
    START = 8
    IN_JAIL_OR_JUST_VISITING = 9
    FREE_PARKING = 10
    IMPRISON = 11
    
class BlockStatus:
    # basic (1 bit)
    DISABLED = 0b0
    ENABLED = 0b1
    # properties (2 bit)
    UNOWNED = 0b000
    OWNED = 0b010
    MORTGAGED = 0b000
    UNMORTGAGED = 0b100


class Block:
    def __init__(self, name, type, index, status):
        self.name = name
        self.type = type
        self.index = index
        self.status = status

class PropertyBlock(Block):
    def __init__(self, name, type, index, purchase_price, mortagate_price, rent_chart, owner, status):
        super(Block).__init__(name, type, index, status)
        self.owner = owner
        # monetary variables
        self.purchase_price = purchase_price
        self.mortagate_price = mortagate_price
        self.rent_chart = rent_chart

class StreetBlock(PropertyBlock):
    def __init__(self, name, index, purchase_price, mortagate_price, house_price_chart, rent_chart, color_group, house_amount, owner = None, status = BlockStatus.ENABLED | BlockStatus.UNOWNED | BlockStatus.UNMORTGAGED):
        super(PropertyBlock).__init__(name, BlockType.STREET, index, purchase_price, mortagate_price, rent_chart, owner, status)
        self.color_group = color_group
        self.house_price_chart = house_price_chart
        self.house_amount = house_amount

class RailroadBlock(PropertyBlock):
    def __init__(self, name, index, purchase_price, mortagate_price, rent_chart, owner = None, status = BlockStatus.ENABLED | BlockStatus.UNOWNED | BlockStatus.UNMORTGAGED):
        super(PropertyBlock).__init__(name, BlockType.RAILROAD, index, purchase_price, mortagate_price, rent_chart, owner, status)

class UtilityBlock(PropertyBlock):
    def __init__(self, name, index, purchase_price, mortagate_price, rent_chart, owner = None, status = BlockStatus.ENABLED | BlockStatus.UNOWNED | BlockStatus.UNMORTGAGED):
        super(PropertyBlock).__init__(name, BlockType.UTILITY, index, purchase_price, mortagate_price, rent_chart, owner, status)

class EventBlock(Block):
    def __init__(self, name, type, index, deck, status):
        super(Block).__init__(name, type, index, status)
        self.deck = deck

class ChanceBlock(EventBlock):
    def __init__(self, name, index, chance_card_deck, status = BlockStatus.ENABLED):
        super(EventBlock).__init__(name, BlockType.CHANCE, index, chance_card_deck, status)

class CommunityChestBlock(EventBlock):
    def __init__(self, name, index, community_chest_deck, status = BlockStatus.ENABLED):
        super(EventBlock).__init__(name, BlockType.COMMUNITY_CHEST, index, community_chest_deck, status)

class TaxBlock(Block):
    def __init__(self, name, type, index, tax, status):
        super(Block).__init__(name, type, index, status)
        self.tax = tax

class LuxuryTaxBlock(TaxBlock):
    def __init__(self, name, index, luxury_tax, status = BlockStatus.ENABLED):
        super(TaxBlock).__init__(name, BlockType.LUXURY_TAX, index, luxury_tax, status)

class IncomeTaxBlock(TaxBlock):
    def __init__(self, name, index, income_tax, status = BlockStatus.ENABLED):
        super(TaxBlock).__init__(name, BlockType.INCOME_TAX, index, income_tax, status)

class StartBlock(Block):
    def __init__(self, name, index, salary, status = BlockStatus.ENABLED):
        super(Block).__init__(name, BlockType.START, index, status)
        self.salary = salary

class InJailOrJustVisitingBlock(Block):
    def __init__(self, name, index, status = BlockStatus.ENABLED):
        super(Block).__init__(name, BlockType.IN_JAIL_OR_JUST_VISITING, index, status)

class FreeParkingBlock(Block):
    def __init__(self, name, index, jackpot, status = BlockStatus.ENABLED):
        super(Block).__init__(name, BlockType.FREE_PARKING, index, status)
        self.jackpot = jackpot

class InJailOrJustVisitingBlock(Block):
    def __init__(self, name, index, status = BlockStatus.ENABLED):
        super(Block).__init__(name, BlockType.IMPRISON, index, status)
