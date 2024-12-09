from block import *
from player import *
from font_machine import *
from utilities import *
from constant import *
from game_status import *
from typing import List, Tuple, Union
from stock import *
import pygame

class ActionMenuWindow:
    def __init__(self, screen_size):
        self.screen_width, self.screen_height = screen_size
        self.window = pygame.transform.scale(pygame.image.load("Assets/action menu/white.png"), (int(self.screen_width * 0.4), int(self.screen_height / 2)))
        # player information
        self.player_name = COMIC_SANS18.render("Name: ", 1, "#000000")
        self.player_balance = COMIC_SANS18.render("Balance: ", 1, "#000000")
        # buttons
        self.sell_button = COMIC_SANS18.render("-SELL-", 1, "#000000", "#FFFF00")
        self.buy_button = COMIC_SANS18.render("-BUY-", 1, "#000000", "#00FF00")
        self.confirm_button = COMIC_SANS18.render("-CONFIRM-", 1, "#000000", "#00FF00")
        self.cancel_button = COMIC_SANS18.render("-CANCEL-", 1, "#000000", "#FF0000")
        self.end_round_button = COMIC_SANS18.render("-END ROUND-", 1, "#000000", "#FF0000")
        # surface position handling
        self.window_rect = self.window.get_rect()
        self.window_rect.topleft = (int(self.screen_width * 0.6), 0)
        self.player_name_rect = self.player_name.get_rect()
        self.player_name_rect.topleft = (int(self.screen_width * 0.6), 0)
        self.player_balance_rect = self.player_balance.get_rect()
        self.player_balance_rect.topleft = (int(self.screen_width * 0.6), 20)
        self.sell_button_rect = self.sell_button.get_rect()
        self.sell_button_rect.topleft = (int(self.screen_width * 0.6), 40)
        self.buy_button_rect = self.buy_button.get_rect()
        self.buy_button_rect.topleft = (self.sell_button_rect.left + self.sell_button_rect.width + 5, 40)
        self.end_round_button_rect = self.end_round_button.get_rect()
        self.end_round_button_rect.topleft = (self.buy_button_rect.left + self.buy_button_rect.width + 5, 40)
        self.confirm_button_rect = self.confirm_button.get_rect()
        self.confirm_button_rect.topleft = (int(self.screen_width * 0.6), 40)
        self.cancel_button_rect = self.cancel_button.get_rect()
        self.cancel_button_rect.topleft = (self.confirm_button_rect.left + self.confirm_button_rect.width + 5, 40)
        #
        self.buy_button_disabled = True
        self.buy_button_disable_mask = pygame.Surface((self.buy_button_rect.width, self.buy_button_rect.height), pygame.SRCALPHA)
        self.buy_button_disable_mask.fill((0, 0, 0, 150))
        # TODO:
    def updateWithPlayer(self, player: Player):
        self.player_name = COMIC_SANS18.render(f'Name: {player.name}', 1, "#000000")
        self.player_balance = COMIC_SANS18.render(f'Balance: {player.balance}', 1, "#000000")
        self.player_name_rect = self.player_name.get_rect()
        self.player_name_rect.topleft = (int(self.screen_width * 0.6), 0)
        self.player_balance_rect = self.player_balance.get_rect()
        self.player_balance_rect.topleft = (int(self.screen_width * 0.6), 20)
    def renderToScreen(self, screen: pygame.Surface, game_status):
        screen.blit(self.window, self.window_rect)
        screen.blit(self.player_name, self.player_name_rect)
        screen.blit(self.player_balance, self.player_balance_rect)
        if game_status == GameStatus.WAIT_FOR_TRANSACTIONS:
            screen.blit(self.sell_button, self.sell_button_rect)
            screen.blit(self.buy_button, self.buy_button_rect)
            if self.buy_button_disabled:
                screen.blit(self.buy_button_disable_mask, self.buy_button_rect)
            screen.blit(self.end_round_button, self.end_round_button_rect)
        elif game_status == GameStatus.SELLING:
            screen.blit(self.confirm_button, self.confirm_button_rect)
            screen.blit(self.cancel_button, self.cancel_button_rect)

class BlockInformation:
    def __init__(self, screen_size):
        self.screen_width, self.screen_height = screen_size
        self.window = pygame.transform.scale(pygame.image.load("Assets/action menu/white.png"), (int(self.screen_width * 0.4), int(self.screen_height / 2)))
        self.window_rect = self.window.get_rect()
        self.window_rect.topleft = (int(self.screen_width * 0.6), int(self.screen_height / 2))
        #
        self.block_name = COMIC_SANS18.render("", 1, "#000000")
        self.block_name_rect = self.block_name.get_rect()
        self.block_name_rect.topleft = (int(self.screen_width * 0.6), int(self.screen_height / 2))
        #
        self.block_owner = COMIC_SANS18.render("", 1, "#000000")
        self.block_owner_rect = self.block_owner.get_rect()
        self.block_owner_rect.topleft = (int(self.screen_width * 0.6), int(self.screen_height / 2) + 20)
        #
        self.block_purchase_price_label = COMIC_SANS18.render("", 1, "#000000")
        self.block_purchase_price_label_rect = self.block_purchase_price_label.get_rect()
        self.block_purchase_price_label_rect.topleft = (int(self.screen_width * 0.6), int(self.screen_height / 2) + 40)
        #
        self.block_purchase_price = COMIC_SANS18.render("", 1, "#000000")
        self.block_purchase_price_rect = self.block_purchase_price.get_rect()
        self.block_purchase_price_rect.topleft = (int(self.screen_width * 0.6), int(self.screen_height / 2) + 60)
        #
        self.block_rent_label = COMIC_SANS18.render("", 1, "#000000")
        self.block_rent_label_rect = self.block_rent_label.get_rect()
        self.block_rent_label_rect.topleft = (int(self.screen_width * 0.6), int(self.screen_height / 2) + 80)
        #
        self.block_rent = COMIC_SANS18.render("", 1, "#000000")
        self.block_rent_rect = self.block_rent.get_rect()
        self.block_rent_rect.topleft = (int(self.screen_width * 0.6), int(self.screen_height / 2) + 100)
        #
    def updateToBlock(self, block: BLOCK, player_list: List[Player]):
        self.block_name = COMIC_SANS18.render(block.name, 1, "#000000")
        self.additional_information = []
        if isinstance(block, StreetBlock):
            owner = player_list[block.owner].name if block.owner != None else None
            self.block_owner = COMIC_SANS18.render(f"Owner: {owner}", 1, "#000000")
            self.block_purchase_price_label = HUNINN18.render(f"SP---1H---2H---3H---4H---5H---", 1, "#000000")
            chart = block.house_price_chart
            self.block_purchase_price = HUNINN18.render(f"{str(block.purchase_price).ljust(5, '-')}{str(chart[0]).ljust(5, '-')}{str(chart[1]).ljust(5, '-')}{str(chart[2]).ljust(5, '-')}{str(chart[3]).ljust(5, '-')}{str(chart[4]).ljust(5, '-')}", 1, "#000000")
            self.block_rent_label = HUNINN18.render(f"SP---1H---2H---3H---4H---5H---", 1, "#000000")
            chart = block.rent_chart
            self.block_rent = HUNINN18.render(f"{str(chart[0]).ljust(5, '-')}{str(chart[1]).ljust(5, '-')}{str(chart[2]).ljust(5, '-')}{str(chart[3]).ljust(5, '-')}{str(chart[4]).ljust(5, '-')}{str(chart[5]).ljust(5, '-')}", 1, "#000000")
        elif isinstance(block, RailroadBlock):
            owner = player_list[block.owner].name if block.owner != None else None
            self.block_owner = COMIC_SANS18.render(f"Owner: {owner}", 1, "#000000")
            self.block_purchase_price_label = HUNINN18.render(f"SP", 1, "#000000")
            self.block_purchase_price = HUNINN18.render(f"{str(block.purchase_price)}", 1, "#000000")
            self.block_rent_label = HUNINN18.render(f"1S---2S---3S---4S---", 1, "#000000")
            chart = block.rent_chart
            self.block_rent = HUNINN18.render(f"{str(chart[0]).ljust(5, '-')}{str(chart[1]).ljust(5, '-')}{str(chart[2]).ljust(5, '-')}{str(chart[3]).ljust(5, '-')}", 1, "#000000")
        elif isinstance(block, UtilityBlock):
            owner = player_list[block.owner].name if block.owner != None else None
            self.block_owner = COMIC_SANS18.render(f"Owner: {owner}", 1, "#000000")
            self.block_purchase_price_label = HUNINN18.render(f"SP", 1, "#000000")
            self.block_purchase_price = HUNINN18.render(f"{str(block.purchase_price)}", 1, "#000000")
            self.block_rent_label = HUNINN18.render(f"1U---2U---", 1, "#000000")
            chart = block.rent_chart
            self.block_rent = HUNINN18.render(f"{str(chart[0]).ljust(5, '-')}{str(chart[1]).ljust(5, '-')}", 1, "#000000")
        else:
            self.block_owner = COMIC_SANS18.render("", 1, "#000000")
            self.block_purchase_price_label = COMIC_SANS18.render("", 1, "#000000")
            self.block_purchase_price = COMIC_SANS18.render("", 1, "#000000")
            self.block_rent_label = COMIC_SANS18.render("", 1, "#000000")
            self.block_rent = COMIC_SANS18.render("", 1, "#000000")
    def renderToScreen(self, screen: pygame.Surface):
        screen.blit(self.window, self.window_rect)
        screen.blit(self.block_name, self.block_name_rect)
        screen.blit(self.block_owner, self.block_owner_rect)
        screen.blit(self.block_rent, self.block_rent_rect)
        screen.blit(self.block_rent_label, self.block_rent_label_rect)
        screen.blit(self.block_purchase_price, self.block_purchase_price_rect)
        screen.blit(self.block_purchase_price_label, self.block_purchase_price_label_rect)

class BoardCenter:
    def __init__(self, board_center_image: pygame.Surface, board_center_rect: pygame.Rect, block_icon_topleft: tuple[int], block_icons: list[tuple[pygame.Surface]]):
        self.window = pygame.transform.scale(board_center_image, (board_center_rect.width, board_center_rect.height))
        self.window_rect = board_center_rect
        # Onselect Block 
        self.block_icon_topleft: tuple[int] = block_icon_topleft
        self.block_icons: List[pygame.Surface] = block_icons
        self.onselect_block: int = None
    def updateSelection(self, block_index: int):
        if block_index == None:
            self.onselect_block = None
        else:
            self.onselect_block = self.block_icons[block_index]
    def renderToScreen(self, screen: pygame.Surface):
        screen.blit(self.window, self.window_rect)
        if self.onselect_block != None:
            screen.blit(self.onselect_block, self.block_icon_topleft)

class StockTransactions:
    def __init__(self, screen_size, market: Market):
        self.screen_width, self.screen_height = screen_size
        self.window = pygame.transform.scale(pygame.image.load("Assets/action menu/white.png"), (int(self.screen_width * 0.4), int(self.screen_height / 4 * 3)))
        self.window_rect = self.window.get_rect()
        self.window_rect.topleft = (int(self.screen_width * 0.6), int(self.screen_height / 4))
        #
        self.market: Market = market
        self.labels = [
            (COMIC_SANS18.render("Market Value", 1, "#000000"), (5, 5)), 
            (COMIC_SANS18.render("stock", 1, "#000000"), (5, 100)), 
            (COMIC_SANS18.render("value", 1, "#000000"), (105, 100)), 
            (COMIC_SANS18.render("owned", 1, "#000000"), (205, 100)), 
            (COMIC_SANS18.render("Transaction on each stock will charge 100 dollars", 1, "#FF0000"), (5, 120 + 20 * self.market.stock_amount))
        ]
        self.prices = []
        self.owned = []
        self.add_buttons = []
        self.minus_buttons = []
        for i, stock_name in enumerate(self.market.market):
            y = 120 + i * 20
            self.labels.append((COMIC_SANS18.render(stock_name, 1, "#000000"), (5, y)))
            self.prices.append([COMIC_SANS18.render("0", 1, "#000000"), addCoordinates((105, y), self.window_rect.topleft)])
            self.owned.append([COMIC_SANS18.render("0", 1, "#000000"), addCoordinates((205, y), self.window_rect.topleft)])
            self.add_buttons.append([COMIC_SANS18.render(" + ", 1, "#000000", "#00FF00"), addCoordinates((305, y), self.window_rect.topleft)])
            self.minus_buttons.append([COMIC_SANS18.render(" - ", 1, "#000000", "#FF0000"), addCoordinates((325, y), self.window_rect.topleft)])
        for label, topleft in self.labels:
            self.window.blit(label, topleft)
        
    def renderToScreen(self, screen: pygame.Surface):
        screen.blit(self.window, self.window_rect)
        for price, rect in self.prices:
            screen.blit(price, rect)
        for owned, rect in self.owned:
            screen.blit(owned, rect)
        for button, rect in self.add_buttons:
            screen.blit(button, rect)
        for button, rect in self.minus_buttons:
            screen.blit(button, rect)    
    def updateToBuyer(self, buyer: Buyer):
        # TODO
        pass
    def getCollideRectAndReactFunctionList(self, now_player: Player):
        rect_and_func = []
        for add, rect in self.add_buttons:
            def trigger_generator(stock_name):
                def trigger():
                    now_player.buyer
            rect_and_func.append(rect, )