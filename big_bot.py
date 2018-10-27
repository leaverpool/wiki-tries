# -*- encoding: utf-8 -*-
import json
import requests
import time
import urllib
import config
from bs4 import BeautifulSoup
import re


TOKEN = "652844002:AAFPHFs48zVNiEoNv9Yp1rpp4l2fmBjOZ20"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js
    print (str(js))

def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


# здесь мы формируем ответные сообщения
def echo_all(updates):
      for update in updates["result"]:
          text = update["message"]["text"]
          print(text)
          if str(text) == "123":
            text = "циферки!"
          if "кого любит Андрей" in text: 
            text = "Настю!"
          if "пошути" in text: 
            text = shutka()
          chat = update["message"]["chat"]["id"]
          send_message(text, chat)
          time.sleep(1)



def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

# главный скрипт
def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(5)

def shutka():
  # парсим итхэппенс и берём случайную хохму
    site = requests.get('https://ithappens.me/random');
    if site.status_code is 200:
      content = BeautifulSoup(site.content, 'html.parser')
      questions = content.find_all(class_='story')
      text = ''.join(BeautifulSoup(str(questions[0]), "html.parser").findAll(text=True))
      m = re.search('\n{5}(.|\n)*?(\.(.|\n)*?noindex)', text)
      bingo = m.group(0)
      m = re.search('\S(.|\n)*?(.|\n)*?(\n\s )', bingo)
      bingo = m.group(0)
      return bingo

if __name__ == '__main__':
    main()




