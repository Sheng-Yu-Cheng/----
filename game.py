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
    def __init__(self, 
            screen_size, 
            board: GameBoard, 
            players: List[Player], 
            action_menu_background_image: pygame.Surface, 
            stock_market: StockMarket, 
            stock_transaction_background_image: pygame.Surface,
            prop_section_background_image: pygame.Surface, 
            block_icons: List[pygame.Surface]
        ):
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
        self.action_menu = ActionMenuWindow(screen_size, action_menu_background_image)
        self.block_information = BlockInformation(screen_size)
        self.stock_transactions = StockTransactions(screen_size, stock_transaction_background_image, stock_market)
        self.board_center = BoardCenter(pygame.image.load("Assets/action menu/white.png"), pygame.Rect(100, 100, 540, 540), (105, 200), block_icons)
        self.prop_section = PropsSection(screen_size, prop_section_background_image, 4)
        self.previous_showing_block_info_index = -1
        #
        self.showing_prop_section = True
        #
        self.dice = Dice()
        self.dice_rolling_counter = 0
        #
        self.status = GameStatus.WAIT_FOR_ROLLING_DICE
        #
        self.collide_rect_and_react_func_list: List[Tuple[pygame.Rect, Callable]] = []
        self.generateCollideRectAndReactFunctionList()
    def renderToScreen(self, screen: pygame.Surface):
        self.action_menu.renderToScreen(screen, self.status)
        self.board.renderToScreen(screen)
        if self.showing_prop_section:
            self.prop_section.renderToScreen(screen)
        else:
            self.stock_transactions.renderToScreen(screen, self.status)
        self.board_center.renderToScreen(screen)
        for player in self.players:
            player.renderToScreen(screen)
        self.block_information.renderToScreen(screen)
        self.dice.renderToScreen(screen)
        if self.status == GameStatus.ROLLING_DICE:
            self.updateDiceStatus()
        elif self.status == GameStatus.WALK_PLAYER_TOKEN:
            self.updatePlayerToken()
        elif self.status == GameStatus.SHOWING_EVENT_CARD:
            self.board.blocks[self.players[self.now_player_index].position].deck.renderToScreen(screen) 
    def generateCollideRectAndReactFunctionList(self, 
            confirm_function: Callable = lambda: False, 
            cancel_function: Callable = lambda: False, 
            block_selection_method: Callable = lambda: False,
            player_selection_method: Callable = lambda: False
        ):
        rect_and_func: List[Tuple[pygame.Rect, Callable]] = []
        rect_and_func.append((self.action_menu.prop_button_rect, self.changeToPropSection))
        rect_and_func.append((self.action_menu.stocks_button_rect, self.changeToStockSection))
        if self.showing_prop_section:
            pass
        else:
            rect_and_func.extend(self.stock_transactions.getCollideRectAndReactFunctionList(self.players[self.now_player_index]))        
        if self.status == GameStatus.WAIT_FOR_ROLLING_DICE:
            rect_and_func.append((self.dice.roll_dice_button_rect, self.startRollDice))
            #
            now_player = self.players[self.now_player_index]
            for prop in now_player.props:
                def propActivateFunctionGenerator(prop: Prop, now_game_state):
                    def trigger():
                        if not prop.need_block_selection and not prop.need_player_selection:
                            self.executePropEffectAndGoBackToGameState(now_game_state)
                            return
                        self.startPropSelection(now_game_state, prop)                        
                        return
                    return trigger
                rect_and_func.append((prop.rect, propActivateFunctionGenerator(prop, self.status)))
        elif self.status == GameStatus.WAIT_FOR_TRANSACTIONS:
            rect_and_func.append((self.action_menu.buy_button_rect, self.buyNowBlock))
            rect_and_func.append((self.action_menu.sell_button_rect, self.startSelling))
            rect_and_func.append((self.action_menu.end_round_button_rect, self.endRound))
            #
            now_player = self.players[self.now_player_index]
            for prop in now_player.props:
                def propActivateFunctionGenerator(prop: Prop, now_game_state):
                    def trigger():
                        if not prop.need_block_selection and not prop.need_player_selection:
                            self.executePropEffectAndGoBackToGameState(now_game_state)
                            return
                        self.startPropSelection(now_game_state, prop)                        
                        return
                    return trigger
                rect_and_func.append((prop.rect, propActivateFunctionGenerator(prop, self.status)))
        elif self.status == GameStatus.SELLING:
            if self.status == GameStatus.SELLING:
                rect_and_func.append((self.action_menu.confirm_button_rect, self.sellSelectedBlocks))
                rect_and_func.append((self.action_menu.cancel_button_rect, self.cancelSelectionAndReturnToTransaction))
            else:
                rect_and_func.append((self.action_menu.cancel_button_rect, self.cancelSelectionAndReturnToTransaction))
            for block in self.board.blocks:
                if not isinstance(block, (StreetBlock, RailroadBlock, UtilityBlock)) or block.owner != self.now_player_index:
                    block.status &= 0b110
                    continue
                block.status |= 0b001
                def trigger_generator(_block: BLOCK):
                    def trigger():
                        self.block_on_selection = _block.index
                        _block.status ^= BlockStatus.SELECTED
                    return trigger
                rect_and_func.append((block.rect, trigger_generator(block)))
        elif self.status == GameStatus.PROP_TARGET_SELECTION:
            rect_and_func.append((self.action_menu.confirm_button_rect, confirm_function))
            rect_and_func.append((self.action_menu.cancel_button_rect, cancel_function))
            for player in self.players:
                icon = player.icon
                if not player_selection_method(self.board, self.now_player_index, self.players):
                    icon.disabled = True
                    continue
                icon.disabled = False
                def trigger_generator(_icon: PlayerIcon):
                    def trigger():
                        _icon.selected = not _icon.selected
                    return trigger
                rect_and_func.append((icon.rect, trigger_generator(icon)))
            for block in self.board.blocks:
                if not block_selection_method(block, self.board, self.now_player_index, self.players):
                    block.status &= 0b110
                    continue
                block.status |= 0b001
                def trigger_generator(_block: BLOCK):
                    def trigger():
                        self.block_on_selection = _block.index
                        _block.status ^= BlockStatus.SELECTED
                    return trigger
                rect_and_func.append((block.rect, trigger_generator(block)))
        elif self.status == GameStatus.SHOWING_EVENT_CARD:
            rect_and_func.append((pygame.Rect(0, 0, self.screen_width, self.screen_height), self.startExecutingEventCardEffect))
        self.collide_rect_and_react_func_list = rect_and_func
    



    # ------------------- END ROUND ---------------------
    def endRound(self):
        self.now_player_index = (self.now_player_index + 1) % self.player_amount
        while self.players[self.now_player_index].stop_round != 0:
            self.players[self.now_player_index].stop_round -= 1
            self.now_player_index = (self.now_player_index + 1) % self.player_amount
        self.action_menu.updateWithPlayer(self.players[self.now_player_index])
        self.prop_section.updateToPlayer(self.players[self.now_player_index])
        self.status = GameStatus.WAIT_FOR_ROLLING_DICE
        self.generateCollideRectAndReactFunctionList()
    

    # ------------------- PROPS ------------------------
    def executePropEffectAndGoBackToGameState(self, game_state, prop: Prop):
        now_player = self.players[self.now_player_index]
        now_block = self.board.blocks[now_player.index]
        selected_blocks = []
        for block in self.board.blocks:
            if block.status & BlockStatus.SELECTED:
                selected_blocks.append(block)
                block.status ^= BlockStatus.SELECTED
            block.status |= BlockStatus.ENABLED
        selected_players = []
        for player in self.players:
            if player.icon.selected:
                selected_players.append(player)
                player.icon.selected = False
            player.icon.disabled = False
        prop.doEffect(now_block, selected_blocks, self.board, now_player, selected_players, self.players)
        now_player.props.remove(prop)
        self.prop_section.updateToPlayer(now_player)
        self.status = game_state
        self.generateCollideRectAndReactFunctionList()
    def cancelPropActivationAndGoBackToGameState(self, game_state):
        for block in self.board.blocks:
            if block.status & BlockStatus.SELECTED:
                block.status ^= BlockStatus.SELECTED
            block.status |= BlockStatus.ENABLED
        for player in self.players:
            player.icon.selected = False
            player.icon.disabled = False
        self.status = game_state
        self.generateCollideRectAndReactFunctionList()
    def startPropSelection(self, game_state, prop: Prop):
        self.status = GameStatus.PROP_TARGET_SELECTION
        def confirmFunction():
            self.executePropEffectAndGoBackToGameState(game_state, prop)
        def cancelFunction():
            self.cancelPropActivationAndGoBackToGameState(game_state)
        self.generateCollideRectAndReactFunctionList(
            confirmFunction, 
            cancelFunction, 
            prop.block_target_filter,
            prop.player_target_filter
        )

    # ------------------- BLOCK INFO ---------------------
    def handleBlockInformationShowing(self, mouse_position):
        target = None
        for block in self.board.blocks:
            if block.rect.collidepoint(mouse_position):
                if block.index != self.previous_showing_block_info_index:
                    target = block
                break
        if target == None:
            self.board_center.updateSelection(None)
        else:
            self.block_information.updateToBlock(target, self.players)
            self.board_center.updateSelection(target.index)
    
    



    # ------------------- PROP and STOCK ACTION MENU ---------------------
    def changeToPropSection(self):
        self.showing_prop_section = True
        self.generateCollideRectAndReactFunctionList()
    def changeToStockSection(self):
        self.showing_prop_section = False
        self.generateCollideRectAndReactFunctionList()





    # ------------------- DICE ---------------------
    def startRollDice(self): 
        self.status = GameStatus.ROLLING_DICE
        self.dice_rolling_counter = 0
        self.generateCollideRectAndReactFunctionList()
    def updateDiceStatus(self):
        if self.dice_rolling_counter % 10 == 0:
            self.dice.rollDice()
            if self.dice_rolling_counter == 100:
                self.playerGoAhead(self.now_player_index, sum(self.dice.dice_result))
                self.startWalkPlayerToken()
        self.dice_rolling_counter += 1
    




    # ------------------- PLAYER POSITION ---------------------
    def startWalkPlayerToken(self):
        self.status = GameStatus.WALK_PLAYER_TOKEN
        self.player_token_moving_counter = 0
        self.generateCollideRectAndReactFunctionList()
    def playerGoAhead(self, player_index, steps):
        now_player = self.players[player_index]
        now_player.position += steps
        now_player.position %= self.block_amount
        return self.board.blocks[now_player.position]
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
                if self.board.blocks[now_player.position].type == BlockType.IMPRISON:
                    now_player.position = now_player.token_position = self.board.prison_block_index
                    now_player.stop_round = 3
                    now_player.token.rect.topleft = addCoordinates(now_block.rect.center, TOKEN_OFFSET[now_player.index])
                elif self.board.blocks[now_player.position].type == BlockType.CHANCE or self.board.blocks[now_player.position].type == BlockType.COMMUNITY_CHEST:
                    now_block = self.board.blocks[now_player.position]
                    now_block.deck.drawCard()
                    self.startShowingEventCard()
                else:
                    self.startTransactionState()
        self.player_token_moving_counter += 1
    




    # ------------------- EVENT CARD ---------------------
    def startShowingEventCard(self):
        self.status = GameStatus.SHOWING_EVENT_CARD
        self.generateCollideRectAndReactFunctionList()
    def startExecutingEventCardEffect(self):
        now_player = self.players[self.now_player_index]
        now_block = self.board.blocks[now_player.position]
        now_card = now_block.deck.now_card
        if now_card.need_selection:
            self.status = GameStatus.PROP_TARGET_SELECTION
            self.generateCollideRectAndReactFunctionList(
                self.confirmEventCardTargetSelection, 
                self.cancelEventCardTargetSelection, 
                now_card.target_filter
            )
        else:
            now_card.doEffect(now_block, [], self.board, now_player, self.players)
            self.startTransactionState()
    def confirmEventCardTargetSelection(self):
        self.selected_blocks = []
        for block in self.board.blocks:
            if block.status & BlockStatus.SELECTED:
                self.selected_blocks.append(block)
                block.status ^= BlockStatus.SELECTED
            block.status |= BlockStatus.ENABLED
        now_player = self.players[self.now_player_index]
        now_block = self.board.blocks[now_player.position]
        now_card = now_block.deck.now_card
        now_card.doEffect(now_block, [], self.board, now_player, self.players)
        self.startTransactionState()
    def cancelEventCardTargetSelection(self):
        for block in self.board.blocks:
            block.status |= BlockStatus.ENABLED
        self.startTransactionState()



    # ------------------- TRANSACTION ---------------------
    def startTransactionState(self):
        self.status = GameStatus.WAIT_FOR_TRANSACTIONS
        self.generateCollideRectAndReactFunctionList()
        now_player = self.players[self.now_player_index]
        now_block = self.board.blocks[now_player.position]
        now_player.bought_this_round = False
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
    


    # ------------------- SELLING ---------------------
    def startSelling(self):
        self.status = GameStatus.SELLING
        self.generateCollideRectAndReactFunctionList()
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
    def cancelSelectionAndReturnToTransaction(self):
        self.status = GameStatus.WAIT_FOR_TRANSACTIONS
        self.generateCollideRectAndReactFunctionList()
        for block in self.board.blocks:
            if not block.status & BlockStatus.ENABLED:
                block.status ^= BlockStatus.ENABLED
            if block.status & BlockStatus.SELECTED:
                block.status ^= BlockStatus.SELECTED
    

    
    # ------------------- BUY ---------------------
    def buyNowBlock(self):
        now_player = self.players[self.now_player_index]
        now_block = self.board.blocks[now_player.position]
        if now_player.bought_this_round or not isinstance(now_block, PROPERTY_BLCOK):
            return
        if now_block.status & BlockStatus.OWNED and now_block.owner == self.now_player_index:
            if now_block.house_amount < 5 and now_player.balance >= now_block.house_price_chart[now_block.house_amount]:
                now_player.balance -= now_block.house_price_chart[now_block.house_amount]
                now_block.house_amount += 1
                now_player.bought_this_round = True
        elif now_player.balance >= now_block.purchase_price:
            now_player.balance -= now_block.purchase_price
            now_block.owner = now_player.index
            now_block.status |= BlockStatus.OWNED
            self.action_menu.buy_button_disabled = True
            now_player.bought_this_round = True
        self.action_menu.updateWithPlayer(self.players[self.now_player_index])
    def debug(self):
        print("Block stats: ", end = '')
        for block in self.board.blocks:
            print(block.status, end = ' ')

