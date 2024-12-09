import random
import math
from typing import List, Dict
import google.generativeai as genai

genai.configure(api_key = "AIzaSyCqTbUjjEGXpwineW2VxfE-aw1Vzk9KW9k")

## Stock的初始化有名稱Stock.stock_name和市值Stock.market_value
## Market的初始化要有一個Stock的list，然後Market.market是以字典紀錄現在各股(key:Stock.stock_name)的市值(value:Stock)，Market.record是以字典紀錄各股(key:string)三天內的市值(value:list(int))
# storeInfo用來更新Market.record
# aiResponse用來生成評論
# ChangeAllByRandom把Market.market裡所有的市值隨機變動
## Buyer的初始化有玩家名稱Buyer.buyer_name和Market，Buyer.player_stock以字典紀錄玩家各股(key:Stock.stock_name)的數量(value:int)
# buyStock跟sellStock都是吃一個stock_name和數量，並更改Buyer.player_stock紀錄的數量然後return收入或支出

class Stock:
    def __init__(self,name: str, market_value: int = 0):
        self.name: str = name
        self.value = market_value
    def debugStock(self):
        return f'Stock Name = {self.name}\tMarket Value = {self.market_value}\n'
    def changeByRandom(self):
        n = random.randint(500,1500)
        n = n / 1000
        self.market_value =math.ceil(self.market_value * n)
            

class Market(Stock):
    def __init__(self, stock_list: List[Stock]):
        self.market: Dict[str, Stock] = {}
        self.stock_amount: int = len(stock_list)
        self.record: Dict[str, List[int]] = {}
        for stock in stock_list:
            self.market[stock.name] = stock
            self.record[stock.name] = ['No data', 'No data', stock.value]
    def storeInfo(self):
        for stock in self.record:
            self.record[stock].pop(0)
            self.record[stock].append(self.market[stock].value)
    def aiResponse(self):
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        prompt = '以下為各股票的名稱以及它們過去三天的市值:\n'
        for i in self.record:
            prompt += f'名稱:{i}\t前天:{self.record[i][0]},昨天:{self.record[i][1]},今天:{self.record[i][2]}\n'
        prompt += '請用大約50字大致分析各股票的情況'
        
        response = model.generate_content(prompt)
        return response.text
        
    def changeAllByRandom(self):
        for i in self.market:
            self.market[i].changeByRandom()
        self.storeInfo()
    def debugMarket(self):
        string = ''
        for i in self.market:
            string += self.market[i].debugStock()
        return string
    def debugRecord(self):
        string = ''
        for i in self.record:
            string += f'Name:{i}\tRecord:{self.record[i]}\n'
        return string


class Buyer(Market):
    def __init__(self,buyer_name:str,Market:Market):
        self.buyer_name = buyer_name
        self.player_stock={}
        for i in Market.market:
            self.player_stock[i] = 0
    def buyStock(self, stock_name:str, number:int, Market:Market):
        self.player_stock[stock_name] += number
        return Market.market[stock_name].market_value*number
    def sellStock(self, stock_name:str, number:int, Market:Market):
        number = min(self.player_stock[stock_name],number)
        self.player_stock[stock_name] -= number
        return Market.market[stock_name].market_value*number
    def debugBuyer(self):
        string = f'Name: {self.buyer_name}\n'
        for i in self.player_stock:
            string += f'{i}: {self.player_stock[i]}\n'
        return string