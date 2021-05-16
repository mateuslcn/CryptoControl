import json
import requests
import websocket # use "pip install websocket-client"
import numpy as np
from MongoDataBaseAccess import *

nextIvalue = 0

def service_url(service_name):
  return 'https://api.coinext.com.br:8443/AP/%s' % service_name

def call_get(service_name, **kwargs):
  res = requests.get(service_url(service_name), **kwargs)
  return json.loads(res.content)

def call_post(service_name, payload={}, **kwargs):
  res = requests.post(service_url(service_name), json.dumps(payload), **kwargs)
  return json.loads(res.content)

def on_error(ws, error):
  print(error)

def show_info(ws, data_string):
  data = json.loads(data_string)
  print('Bitcoin Value:', data['o'][:].split(',')[4])
  bitcoinCurrentValue = data['o'][:].split(',')[4]
  print(personal_services(bitcoinCurrentValue))
  print('TestingPoint')

def start_talking(ws):
  ws.on_message = show_info
  call_service(ws, 'SubscribeTicker', {
    "OMSId": 1, 
    "InstrumentId": 1, # BTCBRL
    "Interval": 60,    # 1 min
    "IncludeLastCount": 10
  })  

def call_service(ws, service_name, data, level=0):
  global nextIvalue
  frame = {
    'm': level,
    'i': nextIvalue,
    'n': service_name,
    'o': json.dumps(data)
  }
  nextIvalue += 2
  ws.send(json.dumps(frame))

def personal_services (bitcoinCurrentValue):
  buyedAt = [values.find_one()['buyedAt'][1:-1].split(',')[0], values.find_one()['buyedAt'][1:-1].split(',')[1]]
  buyedQuantity = [values.find_one()['buyedQuantity'][1:-1].split(',')[0],values.find_one()['buyedQuantity'][1:-1].split(',')[1]]
  realFortune = sum((bitcoinCurrentValue/np.array(buyedAt))*np.array(buyedQuantity)) - sum(np.array(buyedQuantity)) 
  return realFortune

def main():
  auth = call_get('authenticate', auth=(str(coinext_collection.find_one()['login']), str(coinext_collection.find_one()['password'])))
  if auth['Authenticated']:
    user_info = call_post('GetUserInfo', headers={
      'aptoken': auth['Token'],
      'Content-type': 'application/json'
    })
  print(user_info)
  ws = websocket.WebSocketApp('wss://api.coinext.com.br/WSGateway/',
                              on_error=on_error,
                              on_message=show_info,
                              on_open=start_talking)
  ws.run_forever()
  
if __name__ == "__main__":
  main()