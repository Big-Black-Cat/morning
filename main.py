from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
import time
from datetime import datetime, timedelta, timezone

def get_currentdate():
#   return time.strftime('%Y{}%m{}%d{}',
# time.localtime()).format("年","月","日")

  utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
  bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
  dt = bj_dt.strftime("%Y-%m-%d %H:%M:%S")
  dt1 = bj_dt.strftime("%Y")+"年"
  dt2 = bj_dt.strftime("%m")+"月"
  dt3 = bj_dt.strftime("%d")+"日"
  dt4 = bj_dt.strftime("%H:%M:%S")
  localtime=dt1+dt2+dt3+" "+dt4
  return localtime

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']
mybirthday = os.environ['MYBIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


# def get_weather():
#   url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
#   res = requests.get(url).json()
#   weather = res['data']['list'][0]
#   return weather['weather'], math.floor(weather['temp'])
def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp']),math.floor(weather['low']),math.floor(weather['high'])



def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_mybirthday():
  next = datetime.strptime(str(date.today().year) + "-" + mybirthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days



def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
# wea, temperature = get_weather()
# data = {"date_current":{"value":get_currentdate()},"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
wea, temperature ,low_temp, high_temp = get_weather()
data = {"date_current":{"value":get_currentdate()},"weather":{"value":wea},"low_temp":{"value":low_temp},"high_temp":{"value":high_temp},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"mybirthday_left":{"value":get_mybirthday()},"words":{"value":get_words(), "color":get_random_color()}}

res = wm.send_template(user_id, template_id, data)
print(res)
