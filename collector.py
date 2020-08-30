#!/usr/bin/env python3

import os
import sys
import time
import datetime
import math
import RPi.GPIO as GPIO
import dht11
import mysql.connector
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from MySQLConnector.mysqlconnector import MySqlConnector
from MyLogger.mylogger import MyLogger

waitSecondsCount = 12
collect = []
dhtInstance = None
db = None
logger = None

# 初期化
def initalize():
  global db
  global logger
  global dhtInstance
  # GPIOの初期化
  GPIO.setwarnings(True)
  GPIO.setmode(GPIO.BCM)
  # 電源ピンを起動
  GPIO.setup(22, GPIO.OUT)
  GPIO.output(22, GPIO.HIGH)
  dhtInstance = dht11.DHT11(pin=23)
  # create instance
  db = MySqlConnector()
  logger = MyLogger('roomEnv')

  logger.info('started', 'Room Enviroments Collector')

# データ収集
def collectData():
  sensorValues = getSensorValues()
  # collect data
  if sensorValues['valid']:
    print('Valid sensor values', sensorValues)
    collect.append(sensorValues)
  else:
    print('Invalid sensor values')

# データ登録
def registData():
  tt = 0
  th = 0
  ave = {}
  collectLength = len(collect)
  for item in collect:
    tt += item['temp']
    th += item['humi']
  ave['date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  ave['temp'] = math.floor((tt / collectLength) * 10) / 10
  ave['humi'] = math.floor((th / collectLength) * 10) / 10
  db.cur.execute(
    "INSERT INTO RoomEnviroments (createAt, temputure, humidity) VALUES (%(date)s, %(temp)s, %(humi)s)",
    {
      'date': ave['date'],
      'temp': ave['temp'],
      'humi': ave['humi']
    }
  )
  db.conn.commit()

  # put log
  logMes = 'average: { temp: ' + str(ave['temp']) + ', humi: ' + str(ave['humi']) + '}'
  logger.info('registed', logMes)
  # clear collect items
  collect.clear()

def getSensorValues():
  # read sensor values
  result = dhtInstance.read()

  # return result
  if result.is_valid():
    return {
      'valid': True,
      'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
      'temp': result.temperature,
      'humi': result.humidity
    }
  else:
    return {
      'valid': False,
      'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
      'temp': 0,
      'humi': 0
    }

if __name__ == '__main__':
  prevMinute = -1
  try:
    # 初期化
    initalize()
    # 処理ループ
    while True:
      # データ収集
      collectData()
      currentMinute = int(datetime.datetime.now().strftime("%M"))
      if len(collect) > 0 and currentMinute != prevMinute and currentMinute % 10 == 0:
        # 前回から10分経過したとき
        registData()
        # 今回の実行[分]を記録
        prevMinute = currentMinute
      # 12秒待ち
      time.sleep(waitSecondsCount)

  except:
    # put log
    logger.fatal('exception', str(sys.exc_info()))
    
    GPIO.cleanup()
    logger.info('exit', 'GPIO Cleanuped!')
    
    db.close()
    logger.close()
