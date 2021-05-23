import json
import requests
#import websocket # use "pip install websocket-client"
import numpy as np
from MongoDataBaseAccess import *
import yfinance as yf
from pandas import json_normalize
import pandas as pd
import matplotlib
matplotlib.use('TKAgg')
import pandas as pd
import telebot #use pip install pyTelegramBotAPI
import os
import sys
from IPython import get_ipython

nextIvalue = 0
cryptodict = {
  "BTC": "1",
  "LTC": "2", 
  "ETH": "4",
  "XRP": "6", 
  "BCH": "8", 
  "USDT": "10",
  "LINK": "12", 
  "DOGE": "14", 
  "ADA": "16", 
  "EOS": "18",
  "XLM": "20",
}

def service_url(service_name):
  return 'https://api.coinext.com.br:8443/AP/%s' % service_name

def call_get(service_name, **kwargs):
  res = requests.get(service_url(service_name), **kwargs)
  return json.loads(res.content)

def call_post(service_name, payload={}, **kwargs):
  res = requests.post(service_url(service_name), json.dumps(payload), **kwargs)
  return json.loads(res.content)

def get_info(cryptoCurrentValue,cryptoCoin):
  cryptoBalance = personal_services(cryptoCoin, cryptoCurrentValue)
  return cryptoBalance

def personal_services (cryptoCoin,cryptoCurrentValue):

  if cryptoCoin == 'BTC':
    buyedAt = [float(values.find_one()['buyedAt'][1:-1].split(',')[0]), float(values.find_one()['buyedAt'][1:-1].split(',')[1])]
    buyedQuantity = [float(values.find_one()['buyedQuantity'][1:-1].split(',')[0]), float(values.find_one()['buyedQuantity'][1:-1].split(',')[1])]
    realFortune = sum((cryptoCurrentValue/np.array(buyedAt))*np.array(buyedQuantity)) - sum(np.array(buyedQuantity))
    return realFortune

  if cryptoCoin == 'ETH':
    buyedAt = [float(values.find_one()['buyedAt'][1:-1].split(',')[2])]
    buyedQuantity = [float(values.find_one()['buyedQuantity'][1:-1].split(',')[2])]
    realFortune = sum((cryptoCurrentValue/np.array(buyedAt))*np.array(buyedQuantity)) - sum(np.array(buyedQuantity))
    return realFortune

  if cryptoCoin == 'DOGE':
    buyedAt = [float(values.find_one()['buyedAt'][1:-1].split(',')[3]), float(values.find_one()['buyedAt'][1:-1].split(',')[4]), float(values.find_one()['buyedAt'][1:-1].split(',')[5])]
    buyedQuantity = [float(values.find_one()['buyedQuantity'][1:-1].split(',')[3]),float(values.find_one()['buyedQuantity'][1:-1].split(',')[4]), float(values.find_one()['buyedQuantity'][1:-1].split(',')[5])]
    realFortune = sum((cryptoCurrentValue/np.array(buyedAt))*np.array(buyedQuantity)) - sum(np.array(buyedQuantity))
    return realFortune
  else:
    return 'Coin Not Invested'

def ticket_history(ticket):
  
  ticker = yf.Ticker(ticket)
  start = '2021-01-01'
  end = '2021-05-17'
  return ticker.history(period='1d', interval ='1m')['Close']

def obterBooks(coin):
  payload = {
    'OMSId': 1,
    'AccountId': 1,
    'InstrumentId': coin,
    'Depth': 1,
    'StartIndex': 1,
    "Interval": 60,
    'EndDteTime': 151071922297021,
    'BeginDateTime': 151071868195634,
    'TradeTime': 151071868195634 #time.mktime(datetime.datetime(2020,5,10,18,52,47,874766).timetuple())
  }
  return call_post('GetL2Snapshot', payload)

#Telegram bot
bot = telebot.TeleBot(str(values.find_one()['bot']))

def main():
  
  @bot.message_handler(commands=['start', 'help'])
  def send_welcome(message):
    cryptoCoin = ['BTC', 'ETH', 'DOGE']
    soma = []
    report_partial = ''
    title= 'CRYPTOCOIN INVESTMENT INSTANT REPORT \n\n'
    print(title)

    for x in cryptoCoin:
      data=obterBooks(cryptodict[x])
      cryptoCurrentValue= data[0][4]
      print(x, 'Current Value:', '%.2f' % cryptoCurrentValue)
      print('Current Balance:', '%.2f' % get_info(cryptoCurrentValue, x), '\n')
      soma.append(get_info(cryptoCurrentValue, x))
      report_p = str(x) + ' Current Value: R$' + str('%.2f' % cryptoCurrentValue) + \
     '\nCurrent Balance: R$' + str('%.2f' % get_info(cryptoCurrentValue, x)) + '\n'
      report_partial = report_partial + report_p + '\n'
  
    buyedQuantityTotal = [float(values.find_one()['buyedQuantity'][1:-1].split(',')[0]), float(values.find_one()['buyedQuantity'][1:-1].split(',')[1]), float(values.find_one()['buyedQuantity'][1:-1].split(',')[2]), float(values.find_one()['buyedQuantity'][1:-1].split(',')[3]), float(values.find_one()['buyedQuantity'][1:-1].split(',')[4]), float(values.find_one()['buyedQuantity'][1:-1].split(',')[5])]
    print('Initial Investiment=', '%.2f' % sum(buyedQuantityTotal),'\n')
    print('Current Loss=', '%.2f' % sum(soma),'\n')
    print('Total Current Balance=', '%.2f' % (sum(buyedQuantityTotal)+sum(soma)),'\n')
    report_total = 'Initial Investiment = R$' + str('%.2f' % sum(buyedQuantityTotal)) + '\n' \
    'Current Loss = R$' + str('%.2f' % sum(soma)) + '\n' + \
    'Total Current Balance = R$' + str('%.2f' % (sum(buyedQuantityTotal) + sum(soma))) + '\n\n'
    report = title+report_partial+report_total 
    bot.reply_to(message, report)
    bot.stop_polling()
    
  @bot.message_handler(func=lambda message: True)
  def echo_all(message):
	  bot.reply_to(message, message.text)

  bot.polling()    

if __name__ == "__main__":
  while True: main()