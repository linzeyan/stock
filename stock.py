#!/bin/python3
# -*- coding: utf-8 -*-

import time
from datetime import date
import os
import json
import requests
import pandas
from bs4 import BeautifulSoup

"""Get stock info
stock = '1234'
path = 'data'

folder_path = '{}/{}'.format(path, date.today().strftime('%Y%m%d'))
if not os.path.isdir(folder_path):
    os.makedirs(folder_path)

endpoint = 'http://mis.twse.com.tw/stock/api/getStockInfo.jsp'
timestamp = int(time.time() * 1000 + 1000000)
channels = ''.join('tse_{}.tw'.format(stock))
query_url = '{}?_={}&ex_ch={}'.format(endpoint, timestamp, channels)

req = requests.session()
req.get('http://mis.twse.com.tw/stock/index.jsp',headers={'Accept-Language': 'zh-TW'})

response = req.get(query_url)
content = json.loads(response.text)['msgArray']
raw = pandas.DataFrame(content)
raw.to_csv('{}/{}/{}_raw.csv'.format(path, date.today().strftime('%Y%m%d'), stock))

result = pandas.DataFrame(content)[['c','n','o','h','l','tv']].rename(index=str, columns={'c': '代號','n': '名稱','o':'開盤','h':'最高','l':'最低','tv':'當日成交量'})
result.to_csv('{}/{}/{}.csv'.format(path, date.today().strftime('%Y%m%d'), stock))
"""
#for row in content:
#    try:
#        file_path = '{}/{}.csv'.format(folder_path, row['c'])
#        with open(file_path, 'a') as output_file:
#            writer = csv.writer(output_file, delimiter=',')
#            writer.writerow([
#                row['t'],# 資料時間
#                row['z'],# 最近成交價
#                row['tv'],# 當盤成交量
#                row['v'],# 當日累計成交量
#                row['a'],# 最佳五檔賣出價格
#                row['f'],# 最價五檔賣出數量
#                row['b'],# 最佳五檔買入價格
#                row['g']# 最佳五檔買入數量
#            ])
#
#    except Exception as err:
#        print(err)

path = 'files/stock'
folder_path = '{}/{}'.format(path, date.today().strftime('%Y%m%d'))

if not os.path.isdir(folder_path):
      os.makedirs(folder_path)

def get_stock_id():
    data = []
    stock_url = 'http://isin.twse.com.tw/isin/C_public.jsp?strMode=2'
    req = requests.get(stock_url)
    req = BeautifulSoup(req.text, 'html.parser').find_all('tr')
    for row in req:
        columns = row.find_all('td')
        columns = [ele.text.strip() for ele in columns]
        data.append([ele for ele in columns if ele])
    
    data = pandas.DataFrame(data)[:929]
    data.to_csv(path + '/stock_id.csv')



try:
    data = pandas.DataFrame.from_csv(path +'/stock_id.csv')[2:929]
    stock_id = data['0'].tolist()
except:
    get_stock_id()
    data = pandas.DataFrame.from_csv(path +'/stock_id.csv')[2:929]
    stock_id = data['0'].tolist()

for number in stock_id:
    stock = number.split( )[0]

    try:
        endpoint = 'http://mis.twse.com.tw/stock/api/getStockInfo.jsp'
        timestamp = int(time.time() * 1000 + 1000000)
        channels = ''.join('tse_{}.tw'.format(stock))
        query_url = '{}?_={}&ex_ch={}'.format(endpoint, timestamp, channels)
        print('Query stock: '+stock)
    
        req = requests.session()
        req.get('http://mis.twse.com.tw/stock/index.jsp',headers={'Accept-Language': 'zh-TW'})
    
        response = req.get(query_url)
        content = json.loads(response.text)['msgArray']
        raw = pandas.DataFrame(content)
        raw.to_csv('{}/{}/{}_raw.csv'.format(path, date.today().strftime('%Y%m%d'), stock))
    
        result = pandas.DataFrame(content)[['c','n','o','h','l','tv']].rename(index=str, columns={'c': '代號','n': '名稱','o':'開盤','h':'最高','l':'最低','tv':'當日成交量'})
        result.to_csv('{}/{}/{}.csv'.format(path, date.today().strftime('%Y%m%d'), stock))
    except KeyError:
        print('Error ! stock : '+stock+' need to query again.')
        continue


print('All done')
