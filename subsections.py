from block import *
from player import *
from font_machine import *
from utilities import *
from constant import *
from game_status import *
from typing import List, Tuple, Union
from prop import *
from stock import *
import pygame

class ActionMenuWindow:
    def __init__(self, screen_size, background_image: pygame.Surface):
        self.screen_width, self.screen_height = screen_size
        self.window = pygame.transform.scale(background_image, (int(self.screen_width * 0.4), int(self.screen_height / 2)))
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
        self.prop_button = COMIC_SANS18.render("-PROPS-", 1, "#000000", "#0000FF")
        self.prop_button_rect = self.prop_button.get_rect()
        self.prop_button_rect.topleft = addCoordinates(self.window_rect.topleft, (5, 80))
        self.stocks_button = COMIC_SANS18.render("-STOCKS-", 1, "#000000", "#0000FF")
        self.stocks_button_rect = self.stocks_button.get_rect()
        self.stocks_button_rect.topleft = addCoordinates(self.window_rect.topleft, (105, 80))
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
        screen.blit(self.prop_button, self.prop_button_rect)
        screen.blit(self.stocks_button, self.stocks_button_rect)
        if game_status == GameStatus.WAIT_FOR_TRANSACTIONS:
            screen.blit(self.sell_button, self.sell_button_rect)
            screen.blit(self.buy_button, self.buy_button_rect)
            if self.buy_button_disabled:
                screen.blit(self.buy_button_disable_mask, self.buy_button_rect)
            screen.blit(self.end_round_button, self.end_round_button_rect)
        elif game_status == GameStatus.SELLING:
            screen.blit(self.confirm_button, self.confirm_button_rect)
            screen.blit(self.cancel_button, self.cancel_button_rect)
        elif game_status == GameStatus.PROP_TARGET_SELECTION:
            screen.blit(self.confirm_button, self.confirm_button_rect)
            screen.blit(self.cancel_button, self.cancel_button_rect)

class BlockInformation:
    def __init__(self, screen_size):
        self.screen_width, self.screen_height = screen_size
        self.window = pygame.transform.scale(pygame.image.load("Assets/TaiwanBoard/raw/white.png"), (int(self.screen_width * 0.184), int(self.screen_height * 0.6)))
        self.window_rect = self.window.get_rect()
        self.window_rect.topleft = (405, 205)
        #
        self.block_name = COMIC_SANS18.render("", 1, "#000000")
        self.block_name_rect = self.block_name.get_rect()
        self.block_name_rect.topleft = addCoordinates(self.window_rect.topleft, (5, 5))
        #####
        self.block_descriptions: List[pygame.Surface] = [HUNINN18.render("", 1, "#000000") for i in range(30)]
        self.block_description_rects: List[pygame.Rect] = [pygame.Rect(0, 0, 0, 0) for i in range(30)]
        for i, rect in enumerate(self.block_description_rects):
            rect.topleft = addCoordinates(self.window_rect.topleft, (5, 25 + 20 * i))
        self.block_description_lines = 0
        #
        self.block_owner = COMIC_SANS18.render("", 1, "#000000")
        self.block_owner_rect = self.block_owner.get_rect()
        self.block_owner_rect.topleft = addCoordinates(self.window_rect.topleft, (5, 25))
        ######
        self.block_purchase_prices_amount = 0
        self.block_purchase_prices: List[pygame.Surface] = [COMIC_SANS18.render("", 1, "#000000") for i in range(6)]
        self.block_purchase_prices_rects: List[pygame.Rect] = [pygame.Rect(0, 0, 0, 0) for i in range(6)]
        for i, rect in enumerate(self.block_purchase_prices_rects):
            rect.topleft = addCoordinates(self.window_rect.topleft, (5, 45 + 20 * i))
        ######
        self.block_rents_amount = 0
        self.block_rents: List[pygame.Surface] = [COMIC_SANS18.render("", 1, "#000000") for i in range(6)]
        self.block_rents_rects: List[pygame.Rect] = [pygame.Rect(0, 0, 0, 0) for i in range(6)]
        for i, rect in enumerate(self.block_rents_rects):
            rect.topleft = addCoordinates(self.window_rect.topleft, (5, 185 + 20 * i))
        ######
        self.block_now_house_amount = HUNINN18.render("", 1, "#000000")
        self.block_now_house_amount_rect = pygame.Rect(0, 0, 0, 0)
        self.block_now_house_amount_rect.topleft = addCoordinates(self.window_rect.topleft, (5, 325))
    def updateToBlock(self, block: BLOCK, player_list: List[Player]):
        self.block_now_house_amount = HUNINN18.render("", 1, "#000000")
        if block == None:
            self.block_description_lines = 0
            self.block_name = COMIC_SANS18.render("", 1, "#000000")
            self.block_owner = COMIC_SANS18.render("", 1, "#000000")
            self.block_purchase_prices_amount = 0
            self.block_rents_amount = 0
        elif isinstance(block, StreetBlock):
            self.block_description_lines = 0
            self.block_name = COMIC_SANS18.render(block.name, 1, "#000000")
            owner = player_list[block.owner].name if block.owner != None else None
            self.block_owner = COMIC_SANS18.render(f"Owner: {owner}", 1, "#000000")
            self.block_rents_amount = self.block_purchase_prices_amount = 6
            if block.house_amount == 0:
                self.block_now_house_amount = HUNINN18.render(f"目前沒有房子", 1, "#000000")
            elif block.house_amount == 5:
                self.block_now_house_amount = HUNINN18.render(f"目前有一棟旅館", 1, "#000000")
            else:
                self.block_now_house_amount = HUNINN18.render(f"目前房子數量：{block.house_amount}", 1, "#000000")
            self.block_purchase_prices[0] = HUNINN18.render(f"空地：{block.purchase_price}", 1, "#000000")
            chart = block.house_price_chart
            for i, value in enumerate(chart):
                if i == 4:
                    self.block_purchase_prices[i + 1] = HUNINN18.render(f"旅館：{value}", 1, "#000000")
                else:
                    self.block_purchase_prices[i + 1] = HUNINN18.render(f"第{i + 1}棟房子：{value}", 1, "#000000")
            chart = block.rent_chart
            for i, value in enumerate(chart):
                if i == 0:
                    self.block_rents[i] = HUNINN18.render(f"空地：{value}", 1, "#000000")
                elif i == 5:
                    self.block_rents[i] = HUNINN18.render(f"旅館：{value}", 1, "#000000")
                else:
                    self.block_rents[i] = HUNINN18.render(f"{i}棟房子：{value}", 1, "#000000")
        elif isinstance(block, RailroadBlock):
            self.block_description_lines = 0
            self.block_name = COMIC_SANS18.render(block.name, 1, "#000000")
            owner = player_list[block.owner].name if block.owner != None else None
            self.block_owner = COMIC_SANS18.render(f"Owner: {owner}", 1, "#000000")
            #
            self.block_purchase_prices_amount = 1
            self.block_rents_amount = 4
            self.block_purchase_prices[0] = HUNINN18.render(f"購買價格：{block.purchase_price}", 1, "#000000")
            chart = block.rent_chart
            for i, value in enumerate(chart):
                self.block_rents[i] = HUNINN18.render(f"{i + 1}個車站：{value}", 1, "#000000")
        elif isinstance(block, UtilityBlock):
            self.block_description_lines = 0
            self.block_name = COMIC_SANS18.render(block.name, 1, "#000000")
            owner = player_list[block.owner].name if block.owner != None else None
            self.block_owner = COMIC_SANS18.render(f"Owner: {owner}", 1, "#000000")
            #
            self.block_purchase_prices_amount = 1
            self.block_rents_amount = 2
            self.block_purchase_prices[0] = HUNINN18.render(f"購買價格：{block.purchase_price}", 1, "#000000")
            chart = block.rent_chart
            for i, value in enumerate(chart):
                self.block_rents[i] = HUNINN18.render(f"{i + 1}個電力公司：{value}", 1, "#000000")
        elif block.type == BlockType.BREAD_STORE:
            self.block_description_lines = 0
            self.block_name = COMIC_SANS18.render(block.name, 1, "#000000")
            owner = player_list[block.owner].name if block.owner != None else None
            self.block_owner = COMIC_SANS18.render(f"Owner: {owner}", 1, "#000000")
            self.block_purchase_prices_amount = 1
            self.block_purchase_prices[0] = HUNINN18.render(f"購買價格：{block.purchase_price}", 1, "#000000")
            self.block_rents_amount = 1
            self.block_rents[0] = HUNINN18.render("可惜只能做麵包，沒租金", 1, "#000000")
        else:
            self.block_purchase_prices_amount = self.block_rents_amount = 0
            self.block_name = COMIC_SANS18.render(block.name, 1, "#000000")
            self.block_owner = COMIC_SANS18.render("", 1, "#000000")
            if block.type == BlockType.HARBOR:
                description = "命運與風險交織的邊緣地帶，玩家可選擇走私物品，有機率大賺或被抓進監獄，有機率獲得手槍卡。"
                i, j, self.block_description_lines = 0, 10, 0
                while i < len(description):
                    self.block_descriptions[self.block_description_lines] = HUNINN18.render(description[i:min(j, len(description))], 1, "#000000")
                    self.block_description_lines += 1
                    i += 10
                    j += 10
            elif block.type == BlockType.AIRPORT:
                description = "登上飛機，快速穿梭各地，助你搶占先機！但高空旅行總是充滿未知，風險與機遇並存，做好準備再啟程吧！"
                i, j, self.block_description_lines = 0, 10, 0
                while i < len(description):
                    self.block_descriptions[self.block_description_lines] = HUNINN18.render(description[i:min(j, len(description))], 1, "#000000")
                    self.block_description_lines += 1
                    i += 10
                    j += 10
            elif block.type == BlockType.TAX:
                description = "落在這裡，恭喜你當上大富翁們的「收割大師」！立即向所有玩家徵收5%財產稅，越有錢的對手越讓你笑到合不攏嘴！"
                i, j, self.block_description_lines = 0, 10, 0
                while i < len(description):
                    self.block_descriptions[self.block_description_lines] = HUNINN18.render(description[i:min(j, len(description))], 1, "#000000")
                    self.block_description_lines += 1
                    i += 10
                    j += 10
            elif block.type == BlockType.CHANCE:
                description = "機會只留給勇敢者！這一次，你是否敢於抓住命運的轉捩點？用你的智慧、勇氣和決心，改寫未來，創造屬於自己的奇蹟！"
                i, j, self.block_description_lines = 0, 10, 0
                while i < len(description):
                    self.block_descriptions[self.block_description_lines] = HUNINN18.render(description[i:min(j, len(description))], 1, "#000000")
                    self.block_description_lines += 1
                    i += 10
                    j += 10
            elif block.type == BlockType.COMMUNITY_CHEST:
                description = "命運格，轉動命運的齒輪，抽取一張「命運卡」。可能是一夜暴富的機會，也可能是跌入谷底的挑戰！"
                i, j, self.block_description_lines = 0, 10, 0
                while i < len(description):
                    self.block_descriptions[self.block_description_lines] = HUNINN18.render(description[i:min(j, len(description))], 1, "#000000")
                    self.block_description_lines += 1
                    i += 10
                    j += 10
            elif block.type == BlockType.RENOVATION_COMPARY:
                description = "進入裝修公司的地盤，讓對手的某棟建築停擺！指定一個建築，暫停其過路費收取功能，令對手氣得牙癢癢，卻只能眼睜睜看著收入中斷！"
                i, j, self.block_description_lines = 0, 10, 0
                while i < len(description):
                    self.block_descriptions[self.block_description_lines] = HUNINN18.render(description[i:min(j, len(description))], 1, "#000000")
                    self.block_description_lines += 1
                    i += 10
                    j += 10
            elif block.type == BlockType.PROP_BLOCK:
                description = "道具狂熱！"
                i, j, self.block_description_lines = 0, 10, 0
                while i < len(description):
                    self.block_descriptions[self.block_description_lines] = HUNINN18.render(description[i:min(j, len(description))], 1, "#000000")
                    self.block_description_lines += 1
                    i += 10
                    j += 10
            elif block.type == BlockType.TAX:
                description = "抽稅囉！"
                i, j, self.block_description_lines = 0, 10, 0
                while i < len(description):
                    self.block_descriptions[self.block_description_lines] = HUNINN18.render(description[i:min(j, len(description))], 1, "#000000")
                    self.block_description_lines += 1
                    i += 10
                    j += 10
    def renderToScreen(self, screen: pygame.Surface):
        screen.blit(self.window, self.window_rect)
        screen.blit(self.block_name, self.block_name_rect)
        for i in range(self.block_description_lines):
            screen.blit(self.block_descriptions[i], self.block_description_rects[i])
        screen.blit(self.block_owner, self.block_owner_rect)
        for i in range(self.block_purchase_prices_amount):
            screen.blit(self.block_purchase_prices[i], self.block_purchase_prices_rects[i])
        for i in range(self.block_rents_amount):
            screen.blit(self.block_rents[i], self.block_rents_rects[i])
        screen.blit(self.block_now_house_amount, self.block_now_house_amount_rect)
        

class BoardCenter:
    def __init__(self, 
            board_center_image: pygame.Surface, 
            board_center_rect: pygame.Rect, 
            block_icon_topleft: tuple[int], 
            block_icons: list[pygame.Surface]
        ):
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

class StockNews:
    def __init__(self, screen_size, background_image: pygame.Surface):
        self.screen_width, self.screen_height = screen_size
        self.window = pygame.transform.scale(background_image, (int(self.screen_width * 0.4), int(self.screen_height / 4 * 3)))
        self.window_rect = self.window.get_rect()
        self.window_rect.topleft = (int(self.screen_width * 0.6), int(self.screen_height / 4))


class StockTransactions:
    def __init__(self, screen_size, background_image: pygame.Surface, market: StockMarket):
        self.screen_width, self.screen_height = screen_size
        self.window = pygame.transform.scale(background_image, (int(self.screen_width * 0.4), int(self.screen_height / 4 * 3)))
        self.window_rect = self.window.get_rect()
        self.window_rect.topleft = (int(self.screen_width * 0.6), int(self.screen_height / 4))
        #
        self.market: StockMarket = market
        self.market_value = pygame.transform.scale(pygame.image.load("Assets/TaiwanBoard/Stock/StockChart.png"), (540, 300))
        self.market_value_rect = self.market_value.get_rect()
        self.market_value_rect.topleft = (5, 5)
        self.window.blit(self.market_value, self.market_value_rect)
        self.labels = [ 
            (COMIC_SANS18.render("stock", 1, "#000000"), (5, 305)), 
            (COMIC_SANS18.render("value", 1, "#000000"), (105, 305)), 
            (COMIC_SANS18.render("owned", 1, "#000000"), (205, 305))
        ]
        self.prices: List[List[pygame.Surface, pygame.Rect]] = []
        self.owned: List[List[pygame.Surface, pygame.Rect]] = []
        self.add_buttons: List[List[pygame.Surface, pygame.Rect]] = []
        self.minus_buttons: List[List[pygame.Surface, pygame.Rect]] = []
        y = 0
        for i, stock_name in enumerate(self.market.stocks):
            y = 325 + i * 30
            name = COMIC_SANS18.render(stock_name, 1, "#000000")
            name_rect = name.get_rect()
            name_rect.topleft = (5, y)
            self.labels.append([name, name_rect])
            price = COMIC_SANS18.render("0", 1, "#000000")
            price_rect = price.get_rect()
            price_rect.topleft = addCoordinates((105, y), self.window_rect.topleft)
            self.prices.append([price, price_rect])
            owned = COMIC_SANS18.render("0", 1, "#000000")
            owned_rect = owned.get_rect()
            owned_rect.topleft = addCoordinates((205, y), self.window_rect.topleft)
            self.owned.append([owned, owned_rect])
            add_button = COMIC_SANS18.render(" + ", 1, "#000000", "#00FF00")
            add_button_rect = add_button.get_rect()
            add_button_rect.topleft = addCoordinates((305, y), self.window_rect.topleft)
            self.add_buttons.append([add_button, add_button_rect])
            minus_button = COMIC_SANS18.render(" - ", 1, "#000000", "#FF0000")
            minus_button_rect = minus_button.get_rect()
            minus_button_rect.topleft = addCoordinates((325, y), self.window_rect.topleft)
            self.minus_buttons.append([minus_button, minus_button_rect])
        y += 30
        for label, topleft in self.labels:
            self.window.blit(label, topleft)
        # market value graph
        self.colors = {
            "Foxconn": "#FF0000", 
            "TSMC" : "#FFFF00", 
            "Delta": "#0000FF"
        }
        self.market_value_xcoordinate = [77 + i * 53 + self.window_rect.x for i in range(10)]
        self.market_value_ytop, self.market_value_ybottom = 65, 235
        self.market_value_max, self.market_value_min = 3000, 0
        # 
        self.lines = []
    def updateText(self):
        text = self.market.aiResponse()
        y = 430
        i, j, l = 0, 30 , 0
        self.lines = []
        while j <= len(text):
            self.lines.append((HUNINN18.render(text[i:j], 1, "#000000"), addCoordinates((0, y + 20 * l), self.window_rect.topleft)))
            i += 30
            j += 30
            l += 1
        self.lines.append((HUNINN18.render(text[i:], 1, "#000000"), addCoordinates((0, y + 20 * l), self.window_rect.topleft)))
    def calculateYByValue(self, value):
        return int(self.window_rect.top + self.market_value_ytop + (self.market_value_ybottom - self.market_value_ytop) * (self.market_value_max - value) / (self.market_value_max - self.market_value_min))
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
        for line, rect in self.lines:
            screen.blit(line, rect)
        # draw stock lines
        for record in self.market.record:
            color = self.colors[record]
            record = self.market.record[record]
            i, j = 0, 1
            start_pos = (self.market_value_xcoordinate[0], self.calculateYByValue(record[0]))
            end_pos = (self.market_value_xcoordinate[1], self.calculateYByValue(record[1]))
            while j < 9:
                pygame.draw.line(screen, color, start_pos, end_pos, 2)
                i += 1
                j += 1
                start_pos = end_pos
                end_pos = (self.market_value_xcoordinate[j], self.calculateYByValue(record[j]))
    def updateToPlayer(self, player: Player):
        for i, stock_name in enumerate(self.market.stocks):
            self.prices[i][0] = COMIC_SANS18.render(f'{self.market.stocks[stock_name].value}', 1, "#000000")
            self.owned[i][0] = COMIC_SANS18.render(f'{player.stock_account.stocks[stock_name]}', 1, "#000000")
    def getCollideRectAndReactFunctionList(self, now_player: Player, action_menu: ActionMenuWindow):
        rect_and_func = []
        def add_button_trigger_generator(stock_name):
            def trigger():
                if now_player.balance >= now_player.stock_account.stock_market.stocks[stock_name].value:
                    now_player.stock_account.stocks[stock_name] += 1
                    now_player.balance -= now_player.stock_account.stock_market.stocks[stock_name].value
                    self.updateToPlayer(now_player)
                    action_menu.updateWithPlayer(now_player)
            return trigger
        def minus_button_trigger_generator(stock_name):
            def trigger():
                if now_player.stock_account.stocks[stock_name] > 0:
                    now_player.stock_account.stocks[stock_name] -= 1
                    now_player.balance += now_player.stock_account.stock_market.stocks[stock_name].value
                    self.updateToPlayer(now_player)
                    action_menu.updateWithPlayer(now_player)
            return trigger
        for i, stock_name in enumerate(self.market.stocks):
            add, rect = self.add_buttons[i]
            rect_and_func.append((rect, add_button_trigger_generator(stock_name)))
            minus, rect = self.minus_buttons[i]
            rect_and_func.append((rect, minus_button_trigger_generator(stock_name)))
        return rect_and_func

class PropsSection:
    def __init__(self, screen_size, background_image, prop_amount_limit: int):
        self.screen_width, self.screen_height = screen_size
        self.window = pygame.transform.scale(background_image, (int(self.screen_width * 0.4), int(self.screen_height / 4 * 3)))
        self.window_rect = self.window.get_rect()
        self.window_rect.topleft = (int(self.screen_width * 0.6), int(self.screen_height / 4))
        #
        self.prop_amount_limit = prop_amount_limit
        self.props_list: List[Prop] = []
        self.props_list_topleft: List[Tuple[int]] = []
        for i in range(0, self.prop_amount_limit):
            self.props_list_topleft.append((20 + (i % 2) * 200, 30 + (i >> 1) * 240))
        #
        self.on_viewing_prop_index = -1
        self.prop_info_mask = pygame.Surface((180, 240))
        self.prop_info_mask.fill((255, 255, 255))
        self.prop_info_lines = 0
        self.prop_info: List[pygame.Surface] = [HUNINN18.render("", 1, "#000000") for _ in range(10)]
        self.prop_info_rects: List[pygame.Rect] = [(3, 3 + 20 * i) for i in range(10)]

    def updateToPlayer(self, player: Player):
        self.props_list = player.props
        for i, prop in enumerate(self.props_list):
            prop.setTopleft(addCoordinates(self.window_rect.topleft, self.props_list_topleft[i]))
    def updateToPropInfo(self, prop_info):
        i, j, self.prop_info_lines = 0, 10, 0
        while i < len(prop_info):
            self.prop_info[self.prop_info_lines] = HUNINN18.render(prop_info[i:min(j,len(prop_info))], 1, '#000000')
            i += 10
            j += 10
            self.prop_info_lines += 1
    def handleMousePosition(self, mouse_pos):
        new_collide = -1
        for i, prop in enumerate(self.props_list):
            if prop.rect.collidepoint(mouse_pos):
                new_collide = i
        if new_collide != self.on_viewing_prop_index:
            self.on_viewing_prop_index = new_collide
            if self.on_viewing_prop_index != -1:
                self.updateToPropInfo(self.props_list[i].description)
            
            
    def renderToScreen(self, screen: pygame.Surface):
        screen.blit(self.window, self.window_rect)
        for i, prop in enumerate(self.props_list):
            if self.on_viewing_prop_index == i:
                topleft = prop.rect.topleft
                screen.blit(self.prop_info_mask, topleft)
                for i in range(self.prop_info_lines):
                    screen.blit(self.prop_info[i], addCoordinates(topleft, self.prop_info_rects[i]))
            else:
                prop.renderToScreen(screen)
            
    