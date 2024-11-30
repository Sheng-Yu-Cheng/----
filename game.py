from block import *
from player import *
from game_board import *
from subsections import *
from game_status import *
from dice import *
from constant import *
from typing import List, Union, Callable

class Game:
    def __init__(self, screen_size, board: GameBoard, players: List[Player], status = GameStatus.WAIT_FOR_ROLLING_DICE):
        self.screen_width, self.screen_height = screen_size
        self.board = board
        self.block_amount = len(self.board.blocks)
        self.player_amount = len(players)
        self.players: List[Player] = players
        self.action_menu = ActionMenuWindow(screen_size)
        self.block_information = BlockInformation(screen_size)
        #
        self.dice = Dice()
        self.dice_rolling_counter = 0
        #
        self.status = status
        self.status_changed = False
        #
        self.now_player_index = 0
        self.block_on_selection = -1
        self.previous_showing_block_info_index = -1
    def playerGoAhead(self, player_index, steps):
        self.players[player_index].position += steps
        self.players[player_index].position %= self.block_amount
        return self.blocks[self.players[player_index].position]
    def renderToScreen(self, screen: pygame.Surface):
        self.action_menu.renderToScreen(screen, self.status)
        self.board.renderToScreen(screen)
        self.block_information.renderToScreen(screen)
        if self.status == GameStatus.ROLLING_DICE:
            self.updateDiceStatus()
        self.dice.renderToScreen(screen)
    def generateCollideRectAndFunctionList(self):
        rect_and_func: List[Tuple[pygame.Rect, Callable]] = []
        if self.status == GameStatus.WAIT_FOR_ROLLING_DICE:
            rect_and_func.append((self.dice.roll_dice_button_rect, self.startRollDice))
        elif self.status == GameStatus.SELLING or self.status == GameStatus.MORTGAGING:
            for block in self.board.blocks:
                if not isinstance(block, (StreetBlock, RailroadBlock, UtilityBlock)) or block.owner != self.now_player_index:
                    block.status &= 0b1110
                    continue
                block.status |= 0b0001
                def generator(blk):
                    def func():
                        self.block_on_selection = blk.index
                        blk.status ^= BlockStatus.SELECTED
                    return func
                rect_and_func.append((block.rect, generator(block)))
        return rect_and_func
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
            self.status = GameStatus.PLAYER_MAKING_MOVE
            self.status_changed = True
        self.dice_rolling_counter += 1
    def sellSelectedBlocks(self):
        for block in self.board.blocks:
            if block.status & BlockStatus.SELECTED:
                owner: Player = self.players[block.owner]
                #
                owner.balance += int(block.purchase_price * SELLING_RATIO)
                block.owner = None
                #
                block.status ^= BlockStatus.SELECTED
    def mortagageSelectedBlocks(self):
        for block in self.board.blocks:
            if block.status & BlockStatus.SELECTED:
                owner: Player = self.players[block.owner]
                #
                owner.balance += block.mortagate_price
                block.owner = None
                #
                block.status ^= BlockStatus.SELECTED
                block.status ^= BlockStatus.UNMORTGAGED
    def buyNowBlock(self):
        pass
    def debug(self):
        print("Block stats: ", end = '')
        for block in self.board.blocks:
            print(block.status, end = ' ')

