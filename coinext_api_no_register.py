import json
import requests
import websocket # use "pip install websocket-client"
import numpy as np
from MongoDataBaseAccess import *

nextIvalue = 0
BTC = 1
LTC = 2 
ETH = 4 
XRP = 6 
BCH = 8 
USDT = 10 
LINK = 12 
DOGE = 14 
ADA = 16 
EOS = 18
XLM = 20

def service_url(service_name):
  return 'https://api.coinext.com.br:8443/AP/%s' % service_name

def call_get(service_name, **kwargs):
  res = requests.get(service_url(service_name), **kwargs)
  return json.loads(res.content)

def call_post(service_name, payload={}, **kwargs):
  res = requests.post(service_url(service_name), json.dumps(payload), **kwargs)
  return json.loads(res.content)

def show_info(cryptoCurrentValue):
  print('Bitcoin Value:', cryptoCurrentValue)
  cryptoBalance = personal_services(cryptoCurrentValue)
  return cryptoBalance

def personal_services (cryptoCoin):
  buyedAt = [int(values.find_one()['buyedAt'][1:-1].split(',')[0]), int(values.find_one()['buyedAt'][1:-1].split(',')[1])]
  buyedQuantity = [int(values.find_one()['buyedQuantity'][1:-1].split(',')[0]),int(values.find_one()['buyedQuantity'][1:-1].split(',')[1])]
  realFortune = sum((cryptoCoin/np.array(buyedAt))*np.array(buyedQuantity)) - sum(np.array(buyedQuantity))
  return realFortune

def obterBooks(coin = BTC):
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

def main():
  data=obterBooks()
  bitcoinCurrentValue= data[0][4]
  print('Bitcoin Balance:', show_info(bitcoinCurrentValue))
  
if __name__ == "__main__":
  main()