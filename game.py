from block import *
from player import *
from game_board import *
from subsections import *
from game_status import *
from dice import *
from constant import *
from utilities import *
from typing import List, Union, Callable


class Game:
    def __init__(self, screen_size, board: GameBoard, players: List[Player], status = GameStatus.WAIT_FOR_ROLLING_DICE):
        self.screen_width, self.screen_height = screen_size
        #
        self.board = board
        self.block_amount = len(self.board.blocks)
        self.block_on_selection = -1
        #
        self.player_amount = len(players)
        self.players: List[Player] = players
        self.now_player_index = 0
        self.player_token_moving_counter = 0
        #
        self.action_menu = ActionMenuWindow(screen_size)
        self.block_information = BlockInformation(screen_size)
        self.previous_showing_block_info_index = -1
        #
        self.dice = Dice()
        self.dice_rolling_counter = 0
        #
        self.status = status
        self.status_changed = False
        #
    def playerGoAhead(self, player_index, steps):
        now_player = self.players[player_index]
        now_player.position += steps
        now_player.position %= self.block_amount
        return self.board.blocks[now_player.position]
    def renderToScreen(self, screen: pygame.Surface):
        self.action_menu.renderToScreen(screen, self.status)
        self.board.renderToScreen(screen)
        self.block_information.renderToScreen(screen)
        if self.status == GameStatus.ROLLING_DICE:
            self.updateDiceStatus()
        elif self.status == GameStatus.WALK_PLAYER_TOKEN:
            self.updatePlayerToken()
        for player in self.players:
            player.renderToScreen(screen)
        self.dice.renderToScreen(screen)
    def generateCollideRectAndFunctionList(self):
        rect_and_func: List[Tuple[pygame.Rect, Callable]] = []
        if self.status == GameStatus.WAIT_FOR_ROLLING_DICE:
            rect_and_func.append((self.dice.roll_dice_button_rect, self.startRollDice))
        elif self.status == GameStatus.WAIT_FOR_TRANSACTIONS:
            rect_and_func.append((self.action_menu.buy_button_rect, self.buyNowBlock))
            rect_and_func.append((self.action_menu.sell_button_rect, self.startSelling))
            rect_and_func.append((self.action_menu.mortagage_button_rect, self.startMortgaging))
            rect_and_func.append((self.action_menu.end_round_button_rect, self.endRound))
        elif self.status == GameStatus.SELLING or self.status == GameStatus.MORTGAGING:
            if self.status == GameStatus.SELLING:
                rect_and_func.append((self.action_menu.confirm_button_rect, self.sellSelectedBlocks))
                rect_and_func.append((self.action_menu.cancel_button_rect, self.cancelSelectionAndReturnToTransaction))
            else:
                rect_and_func.append((self.action_menu.confirm_button_rect, self.mortagageSelectedBlocks))
                rect_and_func.append((self.action_menu.cancel_button_rect, self.cancelSelectionAndReturnToTransaction))
            for block in self.board.blocks:
                if not isinstance(block, (StreetBlock, RailroadBlock, UtilityBlock)) or block.owner != self.now_player_index:
                    block.status &= 0b1110
                    continue
                block.status |= 0b0001
                def trigger_generator(_block: BLOCK):
                    def trigger():
                        self.block_on_selection = _block.index
                        _block.status ^= BlockStatus.SELECTED
                    return trigger
                rect_and_func.append((block.rect, trigger_generator(block)))
        return rect_and_func
    def endRound(self):
        self.now_player_index = (self.now_player_index + 1) % self.player_amount
        self.action_menu.updateWithPlayer(self.players[self.now_player_index])
        self.status = GameStatus.WAIT_FOR_ROLLING_DICE
        self.status_changed = True
    def handleBlockInformationShowing(self, mouse_position):
        for block in self.board.blocks:
            if block.rect.collidepoint(mouse_position):
                if block.index != self.previous_showing_block_info_index:
                    self.block_information.updateToBlock(block, self.players)
                break
    # roll dice button react function
    def startRollDice(self):
        self.status = GameStatus.ROLLING_DICE
        self.dice_rolling_counter = 0
        self.status_changed = True
    # this function will make the dice rolling, it will be called upon each frame
    def updateDiceStatus(self):
        if self.dice_rolling_counter % 10 == 0:
            self.dice.rollDice()
            if self.dice_rolling_counter == 100:
                self.playerGoAhead(self.now_player_index, sum(self.dice.dice_result))
                self.startWalkPlayerToken()
        self.dice_rolling_counter += 1
    def startWalkPlayerToken(self):
        self.status = GameStatus.WALK_PLAYER_TOKEN
        self.status_changed = True
        self.player_token_moving_counter = 0
    def updatePlayerToken(self):
        if self.player_token_moving_counter % 10 == 0:
            now_player = self.players[self.now_player_index]
            now_player.token_position += 1
            if now_player.position == self.block_amount:
                now_player += self.board.blocks[0].salary
            now_player.token_position %= self.block_amount
            #
            now_block = self.board.blocks[now_player.token_position]
            now_player.token.rect.topleft = addCoordinates(now_block.rect.center, TOKEN_OFFSET[now_player.index])
            #
            if now_player.position == now_player.token_position:
                self.startTransactionState()
        self.player_token_moving_counter += 1
    def startTransactionState(self):
        self.status = GameStatus.WAIT_FOR_TRANSACTIONS
        self.status_changed = True
        now_player = self.players[self.now_player_index]
        now_block = self.board.blocks[now_player.position]
        if isinstance(now_block, StreetBlock):
            if now_block.owner == None or (now_block.owner == now_player.index and now_block.house_amount < 5):
                self.action_menu.buy_button_disabled = False
            elif now_block.owner != now_player.index:
                self.action_menu.buy_button_disabled = True
                now_player.balance -= now_block.rent_chart[now_block.house_amount]
                self.players[now_block.owner].balance += now_block.rent_chart[now_block.house_amount]
        elif isinstance(now_block, RailroadBlock):
            if now_block.owner == None:
                self.action_menu.buy_button_disabled = False
            elif now_block.owner != now_player.index:
                self.action_menu.buy_button_disabled = True
                possessed_railroad_amount = 0
                for block in self.board.blocks:
                    if isinstance(block, RailroadBlock) and block.owner == now_block.owner:
                        possessed_railroad_amount += 1
                now_player.balance -= now_block.rent_chart[possessed_railroad_amount - 1]
                self.players[now_block.owner].balance += now_block.rent_chart[possessed_railroad_amount - 1]
        elif isinstance(now_block, UtilityBlock):
            if now_block.owner == None:
                self.action_menu.buy_button_disabled = False
            elif now_block.owner != now_player.index:
                self.action_menu.buy_button_disabled = True
                possessed_utility_amount = 0
                for block in self.board.blocks:
                    if isinstance(block, UtilityBlock) and block.owner == now_block.owner:
                        possessed_utility_amount += 1
                now_player.balance -= now_block.rent_chart[possessed_utility_amount - 1]
                self.players[now_block.owner].balance += now_block.rent_chart[possessed_utility_amount - 1]
        self.action_menu.updateWithPlayer(now_player)
    def startSelling(self):
        self.status = GameStatus.SELLING
        self.status_changed = True
    def sellSelectedBlocks(self):
        for block in self.board.blocks:
            if block.status & BlockStatus.SELECTED:
                owner: Player = self.players[block.owner]
                #
                owner.balance += int(block.purchase_price * SELLING_RATIO)
                block.owner = None
                #
                block.status ^= BlockStatus.SELECTED
                block.status ^= BlockStatus.OWNED
        self.action_menu.updateWithPlayer(self.players[self.now_player_index])
        self.cancelSelectionAndReturnToTransaction()
    def startMortgaging(self):
        self.status = GameStatus.MORTGAGING
        self.status_changed = True
    def mortagageSelectedBlocks(self):
        # TODO:
        for block in self.board.blocks:
            if block.status & BlockStatus.SELECTED:
                owner: Player = self.players[block.owner]
                #
                owner.balance += block.mortagate_price
                block.owner = None
                #
                block.status ^= BlockStatus.SELECTED
                block.status ^= BlockStatus.UNMORTGAGED
        self.action_menu.updateWithPlayer(self.players[self.now_player_index])
        self.cancelSelectionAndReturnToTransaction()
    def buyNowBlock(self):
        now_player = self.players[self.now_player_index]
        now_block = self.board.blocks[now_player.position]
        if not isinstance(now_block, PROPERTY_BLCOK):
            return
        if now_block.status & BlockStatus.OWNED:
            if now_block.house_amount < 5 and now_player.balance >= now_block.house_price_chart[now_block.house_amount]:
                now_player.balance -= now_block.house_price_chart[now_block.house_amount]
                now_block.house_amount += 1
        elif now_player.balance >= now_block.purchase_price:
            now_player.balance -= now_block.purchase_price
            now_block.owner = now_player.index
            now_block.status |= BlockStatus.OWNED
            self.action_menu.buy_button_disabled = True
        self.action_menu.updateWithPlayer(self.players[self.now_player_index])
    def cancelSelectionAndReturnToTransaction(self):
        self.status = GameStatus.WAIT_FOR_TRANSACTIONS
        self.status_changed = True
        for block in self.board.blocks:
            if not block.status & BlockStatus.ENABLED:
                block.status ^= BlockStatus.ENABLED
            if block.status & BlockStatus.SELECTED:
                block.status ^= BlockStatus.SELECTED
    def debug(self):
        print("Block stats: ", end = '')
        for block in self.board.blocks:
            print(block.status, end = ' ')

