import random
import math
from typing import List, Dict
import google.generativeai as genai
import numpy as np
import json
import requests

genai.configure(api_key = "AIzaSyCqTbUjjEGXpwineW2VxfE-aw1Vzk9KW9k")

## Stock的初始化有名稱Stock.name和市值Stock.value
## Market的初始化要有一個Stock的list，然後market.stocks是以字典紀錄現在各股(key:Stock.name)的市值(value:Stock)，Market.record是以字典紀錄各股(key:string)三天內的市值(value:list(int))
# storeInfo用來更新Market.record
# aiResponse用來生成評論
# ChangeAllByRandom把market.stocks裡所有的市值隨機變動
## Buyer的初始化有玩家名稱Buyer.buyer_name和Market，Buyer.player_stock以字典紀錄玩家各股(key:Stock.name)的數量(value:int)
# buyStock跟sellStock都是吃一個name和數量，並更改Buyer.player_stock紀錄的數量然後return收入或支出

class Stock:
    def __init__(self,name:str,value:int):
        self.name=name
        self.value=value
    def debugStock(self):
        return f'Stock Name = {self.name}\tMarket Value = {self.value}\n'
    def changeByRandom(self):
        n=random.randint(800,1250)
        n=n/1000
        self.value = math.ceil(self.value*n)
        self.value = min(3000, max(1, self.value))

class Source():
    def __init__(self,symbol:int,name:str,date:int):
        self.name = name
        url = f'https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date={date}&stockNo={symbol}'
        data = requests.get(url).text
        json_data = json.loads(data)
        Stock_data = json_data['data']
        self.data = [(Stock_data[i][6].replace(',','')) for i in range(len(Stock_data))]
    def debugSource(self):
        return f'名稱:{self.name}\t市值紀錄:[{",".join(self.data)}]\n'

class SourceMarket():
    def __init__(self,source_list:List):
        self.sources=[]
        for source in source_list:
            self.sources.append(source)
    def debugSourceMarket(self):
        string = f''
        for source in self.sources:
            string += source.debugSource()
        return string
        
            
class StockMarket():
    def __init__(self,stock_list:list):
        self.stocks: Dict[str,Stock] = {}
        self.stock_amount = len(stock_list)
        self.record = {}
        for stock in stock_list:
            self.stocks[stock.name] = stock
            self.record[stock.name] = ['No data', 'No data', 'No data', 'No data', 'No data', 'No data', 'No data', 'No data', 'No data',stock.value]
    def storeInfo(self):
        for record in self.record:
            self.record[record].pop(0)
            self.record[record].append(self.stocks[record].value)
    def aiResponse(self):
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        prompt = '以下為各股票的名稱以及它們過去十天的市值:\n'
        for record in self.record:
            prompt += f'名稱:{record}\t{",".join(list(map(lambda x: f"{x}元", self.record[record])))}\n'
        prompt += '請用大約50字大致分析各股票的情況'
        
        response = model.generate_content(prompt)
        return response.text
    def changeAllByRandom(self):
        for stock in self.stocks:
            self.stocks[stock].changeByRandom()
        self.storeInfo()
    def changeByAi(self,marketsource):
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f'以下為範例股票，其中包含名稱以及它們的市值紀錄:\n'
        prompt += marketsource.debugSourceMarket()
        prompt += '以下為各模擬股票的名稱以及它們過去的市值:\n'
        for record in self.record:
            prompt += self.debugRecord()
        prompt += f'請在參考範例股票的資訊後幫我預測各模擬股票的市值(一個在0~3000的整數)，如果關係不顯著可以隨意給合理的數值'
        prompt += f'只要給我預測數值以","隔開的一行字串就好了'
        response = model.generate_content(prompt).text
        #print(response)
        prediction_list = response.split(',')
        i_stock = 0
        for stock in self.stocks:
            self.stocks[stock].value = int(prediction_list[i_stock])
            i_stock+=1
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


class StockMarketAccount():
    def __init__(self,market:StockMarket):
        self.stock_market = market
        self.stocks={}
        self.transaction_record = []
        for stock in market.stocks:
            self.stocks[stock] = 0
    def buyStock(self, name:str, number:int, market:StockMarket):
        self.stocks[name] += number
        self.transaction_record.append((market.stocks[name].name, market.stocks[name].value, number, True))
        return market.stocks[name].value*number
    def sellStock(self, name:str, number:int, market:StockMarket):
        number = min(self.stocks[name],number)
        self.transaction_record.append((market.stocks[name].name, market.stocks[name].value, number, False))
        self.stocks[name] -= number
        return market.stocks[name].value*number
    def debugBuyer(self):
        string = f'Name: {self.name}\n'
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

'''
a = SourceMarket([Source(2330,'台積電',20241212),Source(2303,'聯電',20241212),Source(2454,'聯發科',20241212)])
b = StockMarket([Stock('yee', 500), Stock('haha', 1000)])
for i in range(9):
    b.changeAllByRandom()
print(b.debugRecord())
b.changeByAi(a)
print(b.debugRecord())
'''