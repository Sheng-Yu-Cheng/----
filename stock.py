import random
import math
from typing import List, Dict
import google.generativeai as genai

genai.configure(api_key = "AIzaSyCqTbUjjEGXpwineW2VxfE-aw1Vzk9KW9k")

## Stock的初始化有名稱Stock.name和市值Stock.value
## Market的初始化要有一個Stock的list，然後Market.market是以字典紀錄現在各股(key:Stock.name)的市值(value:Stock)，Market.record是以字典紀錄各股(key:string)三天內的市值(value:list(int))
# storeInfo用來更新Market.record
# aiResponse用來生成評論
# ChangeAllByRandom把Market.market裡所有的市值隨機變動
## Buyer的初始化有玩家名稱Buyer.buyer_name和Market，Buyer.player_stock以字典紀錄玩家各股(key:Stock.name)的數量(value:int)
# buyStock跟sellStock都是吃一個name和數量，並更改Buyer.player_stock紀錄的數量然後return收入或支出

class Stock:
    def __init__(self, name: str, value: int):
        self.name = name
        self.value = value
    def changeByRandom(self):
        n = random.randint(500, 1500)
        n = n / 1000
        self.value = math.ceil(self.value * n)
    #
    def debugStock(self):
        return f'Stock Name = {self.name}\tMarket Value = {self.value}\n'
            

class StockMarket():
    def __init__(self, stocks: List[Stock]):
        self.stocks: Dict[str, Stock] = {}
        self.stock_amount = len(stocks)
        self.record = {}
        for stock in stocks:
            self.stocks[stock.name] = stock
            self.record[stock.name] = ['No data', 'No data', stock.value]
    def storeInfo(self):
        for record in self.record:
            self.record[record].pop(0)
            self.record[record].append(self.stocks[record].value)
    def aiResponse(self):
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        prompt = '以下為各股票的名稱以及它們過去三天的市值:\n'
        for record in self.record:
            prompt += f'名稱:{record}\t前天:{self.record[record][0]},昨天:{self.record[record][1]},今天:{self.record[record][2]}\n'
        prompt += '請用大約50字大致分析各股票的情況'
        
        response = model.generate_content(prompt)
        return response.text
    def changeAllByRandom(self):
        for stock in self.stocks:
            self.stocks[stock].changeByRandom()
        self.storeInfo()
    def debugMarket(self):
        string = ''
        for stock in self.stocks:
            string += self.stocks[stock].debugStock()
        return string
    def debugRecord(self):
        string = ''
        for stock in self.record:
            string += f'Name:{stock}\tRecord:{self.record[stock]}\n'
        return string


class StockMarketAccount:
    def __init__(self, stock_market: StockMarket):
        self.stocks = {}
        self.transaction_record = []
        self.stock_market = stock_market
        for stock in self.stock_market.stocks:
            self.stocks[stock] = 0
    def buyStock(self, name:str, number:int):
        self.stocks[name] += number
        self.transaction_record.append((self.stock_market.stocks[name].name, self.stock_market.stocks[name].value, number, True))
        return self.stock_market.stocks[name].value*number
    def sellStock(self, name:str, number:int):
        number = min(self.stocks[name],number)
        self.transaction_record.append((self.stock_market.stocks[name].name, self.stock_market.stocks[name].value, number, False))
        self.stocks[name] -= number
        return self.stock_market.stocks[name].value*number
    def debugBuyer(self):
        string = ''
        for stock in self.stocks:
            string += f'{stock}: {self.stocks[stock]}\n'
        return string
    def degbugTransaction(self):
        string = ''
        for record in self.transaction_record:
            if record[3] == True:
                string += f'Name:{record[0]}\tValue:{record[1]}\tBuy:{record[2]}\n'
            else:
                string += f'Name:{record[0]}\tValue:{record[1]}\tSell:{record[2]}\n'
        return string
