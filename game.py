from random import randint, shuffle
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
            block_icons: List[pygame.Surface], 
            all_props_generating_function: List[Prop], 
            random_event_card_deck: EventCardDeck
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
        self.stock_source = SourceMarket([Source(2330,'台積電',20241130),Source(2308,'台大電子',20241130),Source(2317,'鴻海',20241130)])
        self.stock_transactions = StockTransactions(screen_size, stock_transaction_background_image, stock_market)
        self.board_center = BoardCenter(pygame.image.load("Assets/action menu/white.png"), pygame.Rect(100, 100, 540, 540), (105, 205), block_icons)
        self.prop_section = PropsSection(screen_size, prop_section_background_image, 4)
        self.previous_showing_block_info_index = -1
        #
        self.showing_prop_section = True
        self.game_over = False
        #
        self.selected_blocks: List[Block] = []
        self.selected_players: List[Player] = []
        #
        self.dice = Dice()
        self.dice_rolling_counter = 0
        #
        self.random_event_card_deck = random_event_card_deck
        self.done_random_event = False
        #
        self.status = GameStatus.WAIT_FOR_ROLLING_DICE
        #
        self.collide_rect_and_react_func_list: List[Tuple[pygame.Rect, Callable]] = []
        for player in self.players:
            player.token.rect.topleft = addCoordinates(self.board.blocks[0].rect.center, TOKEN_OFFSET[player.index])
        self.prop_section.updateToPlayer(self.players[self.now_player_index])
        #
        for i in range(30):
            self.stock_transactions.market.changeAllByRandom()
        self.stock_transactions.updateText()
        self.action_menu.updateWithPlayer(self.players[self.now_player_index])
        self.stock_transactions.updateToPlayer(self.players[self.now_player_index])
        #
        self.all_props_generating_function = all_props_generating_function
        self.generateCollideRectAndReactFunctionList()
    def renderToScreen(self, screen: pygame.Surface):
        self.action_menu.renderToScreen(screen, self.status)
        self.board.renderToScreen(screen)
        if self.showing_prop_section:
            self.prop_section.renderToScreen(screen)
        else:
            self.stock_transactions.renderToScreen(screen)
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
        elif self.status == GameStatus.SHOWING_RANDOM_EVENT_CARD:
            self.random_event_card_deck.renderToScreen(screen) 
    def generateCollideRectAndReactFunctionList(self, 
            confirm_function: Callable = lambda: False, 
            cancel_function: Callable = lambda: False, 
            block_selection_method: Callable = lambda: False,
            player_selection_method: Callable = lambda: False, 
            prop_now_using: Prop = None
        ):
        rect_and_func: List[Tuple[pygame.Rect, Callable]] = []
        rect_and_func.append((self.action_menu.prop_button_rect, self.changeToPropSection))
        rect_and_func.append((self.action_menu.stocks_button_rect, self.changeToStockSection))
        if not self.showing_prop_section:
            rect_and_func.extend(self.stock_transactions.getCollideRectAndReactFunctionList(self.players[self.now_player_index], self.action_menu))        
        if self.status == GameStatus.WAIT_FOR_ROLLING_DICE:
            rect_and_func.append((self.dice.roll_dice_button_rect, self.startRollDice))
            #
            if self.showing_prop_section:
                now_player = self.players[self.now_player_index]
                for prop in now_player.props:
                    def propActivateFunctionGenerator(prop: Prop, now_game_state):
                        def trigger():
                            # if not prop.need_block_selection and not prop.need_player_selection:
                            #     self.executePropEffectAndGoBackToGameState(now_game_state, prop)
                            #     return
                            self.startPropSelection(now_game_state, prop)                        
                            return
                        return trigger
                    rect_and_func.append((prop.rect, propActivateFunctionGenerator(prop, self.status)))
        elif self.status == GameStatus.WAIT_FOR_TRANSACTIONS:
            rect_and_func.append((self.action_menu.buy_button_rect, self.buyNowBlock))
            rect_and_func.append((self.action_menu.sell_button_rect, self.startSelling))
            rect_and_func.append((self.action_menu.end_round_button_rect, self.endRound))
            #
            if self.showing_prop_section:
                now_player = self.players[self.now_player_index]
                for prop in now_player.props:
                    def propActivateFunctionGenerator(prop: Prop, now_game_state):
                        def trigger():
                            # if not prop.need_block_selection and not prop.need_player_selection:
                            #     self.executePropEffectAndGoBackToGameState(now_game_state, prop)
                            #     return
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
                if not player_selection_method(player, self.board, self.now_player_index, self.players):
                    icon.disabled = True
                    continue
                icon.disabled = False
                def trigger_generator(_icon: PlayerIcon):
                    def trigger():
                        if _icon.selected:
                            _icon.selected = False
                            self.selected_players.remove(_icon)
                        else:
                            _icon.selected = True
                            self.selected_players.append(_icon)
                            if len(self.selected_players) > prop_now_using.player_target_maximum:
                                self.selected_players[0].icon.selected = False
                                self.selected_players.pop(0)
                    return trigger
                rect_and_func.append((icon.rect, trigger_generator(icon)))
            for block in self.board.blocks:
                if not block_selection_method(block, self.board, self.now_player_index, self.players):
                    block.status &= 0b110
                    continue
                block.status |= 0b001
                def trigger_generator(_block: BLOCK):
                    def trigger():
                        if _block.status & BlockStatus.SELECTED:
                            self.block_on_selection = _block.index
                            _block.status ^= BlockStatus.SELECTED
                            self.selected_blocks.remove(_block)
                        else:
                            _block.status ^= BlockStatus.SELECTED
                            self.selected_blocks.append(_block)
                            if len(self.selected_blocks) > prop_now_using.block_target_maximum:
                                self.selected_blocks[0].status ^= BlockStatus.SELECTED
                                self.selected_blocks.pop(0)
                    return trigger
                rect_and_func.append((block.rect, trigger_generator(block)))
        elif self.status == GameStatus.SHOWING_EVENT_CARD:
            rect_and_func.append((pygame.Rect(0, 0, self.screen_width, self.screen_height), self.startExecutingEventCardEffect))
        elif self.status == GameStatus.SHOWING_RANDOM_EVENT_CARD:
            rect_and_func.append((pygame.Rect(0, 0, self.screen_width, self.screen_height), self.executeRandomEventCardEffect))    
        self.collide_rect_and_react_func_list = rect_and_func
    



    # ------------------- END ROUND ---------------------
    def endRound(self):
        self.done_random_event = False
        self.players[self.now_player_index].invisible_round = False
        self.players[self.now_player_index].identification = -1
        if self.players[self.now_player_index].balance < 0:
            self.game_over = True
        for block in self.board.blocks:
            if isinstance(block, PROPERTY_BLCOK) and block.rent_disabled_round > 0:
                block.rent_disabled_round -= 1
        self.now_player_index = (self.now_player_index + 1) % self.player_amount
        while self.players[self.now_player_index].stop_round != 0:
            self.players[self.now_player_index].stopRoundCountDown()
            self.now_player_index = (self.now_player_index + 1) % self.player_amount
        now_player = self.players[self.now_player_index]
        self.action_menu.updateWithPlayer(now_player)
        self.prop_section.updateToPlayer(now_player)
        # self.stock_transactions.market.changeByAi(self.stock_source)
        self.stock_transactions.market.changeAllByRandom()
        self.stock_transactions.updateText()
        self.stock_transactions.updateToPlayer(now_player)
        if now_player.airport_designated_destination != -1:
            now_player.position = now_player.airport_designated_destination
            now_player.airport_designated_destination = -1
            self.startWalkPlayerToken()
        else:
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
            player.icon.disabled = True
        prop.doEffect(now_block, selected_blocks, self.board, now_player, selected_players, self.players)
        if prop in now_player.props:
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
            player.icon.disabled = True
        self.status = game_state
        self.generateCollideRectAndReactFunctionList()
    def startPropSelection(self, game_state, prop: Prop):
        self.selected_blocks = []
        self.selected_players = []
        self.status = GameStatus.PROP_TARGET_SELECTION
        def confirmFunction():
            self.executePropEffectAndGoBackToGameState(game_state, prop)
        def cancelFunction():
            self.cancelPropActivationAndGoBackToGameState(game_state)
        self.generateCollideRectAndReactFunctionList(
            confirmFunction, 
            cancelFunction, 
            prop.block_target_filter,
            prop.player_target_filter, 
            prop
        )

    # ------------------- BLOCK/PROP INFO ---------------------
    def handlePropInformationShowing(self, mouse_position):
        self.prop_section.handleMousePosition(mouse_position)
    def handleBlockInformationShowing(self, mouse_position):
        target = None
        for block in self.board.blocks:
            if block.rect.collidepoint(mouse_position):
                if block.index != self.previous_showing_block_info_index:
                    target = block
                break
        if target == None:
            self.block_information.updateToBlock(None, self.players)
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
        if not self.done_random_event and random.randint(1, 100) >= 80:
            self.done_random_event = True
            self.random_event_card_deck.drawCard()
            self.startShowingRandomEventCard()
        else:
            self.status = GameStatus.ROLLING_DICE
            self.dice_rolling_counter = 0
            self.generateCollideRectAndReactFunctionList()
    def updateDiceStatus(self):
        if self.dice_rolling_counter % 10 == 0:
            self.dice.rollDice()
            if self.dice_rolling_counter == 100:
                steps = sum(self.dice.dice_result)
                if self.players[self.now_player_index].double_steps:
                    steps <<= 1
                    self.players[self.now_player_index].double_steps = False
                elif self.players[self.now_player_index].half_steps:
                    steps >>= 1
                    self.players[self.now_player_index].double_steps = False
                self.playerGoAhead(self.now_player_index, steps)
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
            if now_player.token_position == self.block_amount:
                now_player += self.board.blocks[0].salary
            now_player.token_position %= self.block_amount
            #
            now_block = self.board.blocks[now_player.token_position]
            now_player.token.rect.topleft = addCoordinates(now_block.rect.center, TOKEN_OFFSET[now_player.index])
            if now_block.has_barrier:
                now_player.position = now_player.token_position
                now_block.has_barrier = False
            if now_block.has_bomb and not now_player.invisible_round:
                now_block.has_bomb = False
                now_player.decreaseHealthPoint(80)
                if now_player.health_points <= 0:
                    self.endRound()
            #
            if now_player.position == now_player.token_position:
                now_block = self.board.blocks[now_player.position]
                if now_block.type == BlockType.IN_JAIL_OR_JUST_VISITING:
                    now_player.stop_round = 3
                    self.endRound()
                elif now_block.type == BlockType.CHANCE or now_block.type == BlockType.COMMUNITY_CHEST:
                    now_block = self.board.blocks[now_player.position]
                    now_block.deck.drawCard()
                    self.startShowingEventCard()
                elif now_block.type == BlockType.AIRPORT:
                    def updateAirportSelection(block, selected_blocks: List[BLOCK], board, now_player: Player, selected_players, players):
                        if len(selected_blocks) == 1:
                            now_player.airport_designated_destination = selected_blocks[0].index
                    airport = Prop(
                        "Airport", 
                        pygame.Surface((1, 1)), 
                        "", 
                        True, 
                        lambda block, y, z, w: block.type != BlockType.AIRPORT, 
                        1, 
                        False,
                        lambda w, x, y, z: False, 
                        0, 
                        updateAirportSelection
                    )
                    self.startPropSelection(GameStatus.WAIT_FOR_TRANSACTIONS, airport)
                elif now_block.type == BlockType.PROP_BLOCK:
                    if len(now_player.props) < 4:
                        shuffle(self.all_props_generating_function)
                        now_player.props.append(self.all_props_generating_function[0]())
                        self.prop_section.updateToPlayer(now_player)
                    self.startTransactionState()
                elif now_block.type == BlockType.TAX:
                    add = 0
                    for player in self.players:
                        if player.index != self.now_player_index:
                            add += int(player.balance * 0.05)
                            player.balance = int(player.balance * 0.95)
                    self.players[self.now_player_index].balance += add
                    self.startTransactionState()
                elif now_block.type == BlockType.HARBOR:
                    def harborEvent(block, selected_blocks: List[BLOCK], board: GameBoard, now_player: Player, selected_players, players):
                        if randint(1, 100) > 60:
                            now_player.position = now_player.token_position = board.prison_block_index
                            now_block = board.blocks[board.prison_block_index]
                            now_player.stop_round = 3
                            now_player.token.rect.topleft = addCoordinates(now_block.rect.center, TOKEN_OFFSET[now_player.index])
                        else:
                            bread_stores = 0
                            for block in self.board.blocks:
                                if isinstance(block, BreadStoreBlock) and block.owner == now_player:
                                    bread_stores += 1
                            now_player.balance += randint(8000, 30000) * (1 << bread_stores)
                    harbor = Prop(
                        "Harbor", 
                        pygame.Surface((1, 1)), 
                        "", 
                        True, 
                        lambda w, x, y, z: False, 
                        0, 
                        False,
                        lambda w, x, y, z: False, 
                        0, 
                        harborEvent
                    )
                    self.startPropSelection(GameStatus.WAIT_FOR_TRANSACTIONS, harbor)                    
                elif now_block.type == BlockType.RENOVATION_COMPARY:
                    def renovation(block, selected_blocks: List[BLOCK], board, now_player: Player, selected_players, players):
                        if len(selected_blocks) == 1:
                            selected_blocks[0].rent_disabled_round = 12
                    renovation_company = Prop(
                        "RenovationCompany", 
                        pygame.Surface((1, 1)), 
                        "", 
                        True, 
                        lambda block, board, now_player_index, players: 
                            isinstance(block, PROPERTY_BLCOK) and 
                            block.owner != now_player_index and
                            block.owner != None, 
                        1, 
                        False,
                        lambda w, x, y, z: False, 
                        0, 
                        renovation
                    )
                    self.startPropSelection(GameStatus.WAIT_FOR_TRANSACTIONS, renovation_company)
                else:
                    self.startTransactionState()
        self.player_token_moving_counter += 1
    
    # ----------------- RANDOM EVENT CARD ----------------
    def startShowingRandomEventCard(self):
        self.status = GameStatus.SHOWING_RANDOM_EVENT_CARD
        self.generateCollideRectAndReactFunctionList()
    def executeRandomEventCardEffect(self):
        now_player = self.players[self.now_player_index]
        now_block = self.board.blocks[now_player.position]
        now_card = self.random_event_card_deck.now_card
        now_card.doEffect(now_block, [], self.board, now_player, [], self.players)
        now_card = self.random_event_card_deck.now_card = None
        self.startRollDice()

    # ------------------- EVENT CARD ---------------------
    def startShowingEventCard(self):
        self.status = GameStatus.SHOWING_EVENT_CARD
        self.generateCollideRectAndReactFunctionList()
    def startExecutingEventCardEffect(self):
        now_player = self.players[self.now_player_index]
        now_block = self.board.blocks[now_player.position]
        now_card = now_block.deck.now_card
        if now_card.need_block_selection or now_card.need_player_selection:
            self.status = GameStatus.PROP_TARGET_SELECTION
            self.generateCollideRectAndReactFunctionList(
                self.confirmEventCardTargetSelection, 
                self.cancelEventCardTargetSelection, 
                now_card.block_target_filter, 
                now_card.player_target_filter, 
                now_card
            )
            now_block.deck.now_card = None
        else:
            now_card.doEffect(now_block, [], self.board, now_player, [], self.players)
            now_block.deck.now_card = None
            self.startTransactionState()
    def confirmEventCardTargetSelection(self):
        self.selected_blocks = []
        self.selected_players = []
        for player in self.players:
            if player.icon.selected:
                self.selected_players.append(player)
        for block in self.board.blocks:
            if block.status & BlockStatus.SELECTED:
                self.selected_blocks.append(block)
                block.status ^= BlockStatus.SELECTED
            block.status |= BlockStatus.ENABLED
        now_player = self.players[self.now_player_index]
        now_block = self.board.blocks[now_player.position]
        now_card = now_block.deck.now_card
        now_card.doEffect(now_block, self.selected_blocks, self.board, self.selected_players, now_player, self.players)
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
                if now_player.identification == -1:
                    if now_block.rent_disabled_round == 0:
                        now_player.balance -= now_block.rent_chart[now_block.house_amount]
                        self.players[now_block.owner].balance += now_block.rent_chart[now_block.house_amount]
                else:
                    if now_block.rent_disabled_round == 0:
                        self.players[now_player.identification].balance -= now_block.rent_chart[now_block.house_amount]
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
                if now_player.identification == -1:
                    if now_block.rent_disabled_round == 0:
                        now_player.balance -= now_block.rent_chart[possessed_railroad_amount - 1]
                        self.players[now_block.owner].balance += now_block.rent_chart[possessed_railroad_amount - 1]
                else:
                    if now_block.rent_disabled_round == 0:
                        self.players[now_player.identification].balance -= now_block.rent_chart[possessed_railroad_amount - 1]
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
                if now_player.identification == -1:
                    if now_block.rent_disabled_round == 0:
                        now_player.balance -= now_block.rent_chart[possessed_utility_amount - 1]
                        self.players[now_block.owner].balance += now_block.rent_chart[possessed_utility_amount - 1]
                else:
                    if now_block.rent_disabled_round == 0:
                        self.players[now_player.identification].balance -= now_block.rent_chart[possessed_utility_amount - 1]
                        self.players[now_block.owner].balance += now_block.rent_chart[possessed_utility_amount - 1]
        elif isinstance(now_block, BreadStoreBlock):
            if now_block.owner == None:
                self.action_menu.buy_button_disabled = False
            elif now_block.owner != now_player.index:
                self.action_menu.buy_button_disabled = True
        else:
            self.action_menu.buy_button_disabled = True
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
        if now_player.bought_this_round or not isinstance(now_block, (PROPERTY_BLCOK, BreadStoreBlock)):
            return
        if now_block.status & BlockStatus.OWNED and now_block.owner == self.now_player_index and isinstance(now_block, StreetBlock):
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

