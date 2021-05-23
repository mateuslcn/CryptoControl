from MongoDataBaseAccess import *
import json
import requests
import numpy as np
import yfinance as yf
from pandas import json_normalize
import pandas as pd
import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import telebot #pip install pyTelegramBotAPI
import os
import coinext_api_no_register as co

#def ticket_history(ticket):
  
#  ticker = yf.Ticker(ticket)
#  start = '2021-01-01'
# end = '2021-05-17'
#  data = ticker.history(period='1d', interval ='1m')
  #data = ticker.history(period='1y', interval ='1d')['Close'].plot()
  #data = ticker.history(interval='1d', start=start, end=end)['Close'].plot()

# data_close = data['Close']
#  return data['Close']

#def main():
#  data_plot = ticket_history('USDBRL=X')
#  x =np.linspace(0,20,100)
  #plt.plot(x,np.sin(x))
  #plt.show()

#if __name__ == "__main__":
#  main()
#  x = sum([0,20,100]) 
#  message = 'dasdasd '+ str(sum([0,20,100])) + \
#  ' isso ae \n' + 'começo da 2alinha \n' + 'etc'
#print(message)

#print(str(coinext_collection.find_one()['login']))#testing srt
#print('password: ', coinext_collection.find_one()['password'])

#print('testing values',values.find_one()['buyedAt'][1:-1].split(',')[0], values.find_one()['buyedAt'][1:-1].split(',')[1])
#print('testing values',values.find_one()['buyedQuantity'][1:-1].split(',')[0], values.find_one()['buyedQuantity'][1:-1].split(',')[1])

def main():
  i=0
  while True:
    co.main()
    i=i+1
    print('pass',i)

main()