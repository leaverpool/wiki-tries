# -*- encoding: utf-8 -*-
import json
import requests
import time
import urllib
import config
import datetime
from bs4 import BeautifulSoup
import re
import random
import csv

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
        #print(str(update))  # {'update_id': 427648189, 'message': {'message_id': 1107, 'from': {'id': 292397556, 'is_bot': False, 'first_name': 'Андрей', 'last_name': 'Левчук', 'username': 'ErugoPurakushi', 'language_code': 'ru'}, 'chat': {'id': 292397556, 'first_name': 'Андрей', 'last_name': 'Левчук', 'username': 'ErugoPurakushi', 'type': 'private'}, 'date': 1540835172, 'text': 'ABC'}}
        number_of_exceptions = 0



        message_was_sent = 0
        try:  # пробуем поймать TEXT из входящего сообщения
            text = update["message"]["text"]
            #text = 'Сорян, не тот тип входящего сообщения...'
            print(str(datetime.datetime.now()) + ': ' + str(text))  # 2018-10-29 20:46:15.614076: ABC

            if str(text) == "123":
                send_message("циферки!", update["message"]["chat"]["id"])

            elif re.search('(прив)|(хэй)|(здрав)|(добрый)|(hi)|(hello)', str(text), re.IGNORECASE):
                send_message("""Привет! Это тестовый бот, но он уже кое-что умеет (например, постить баяны с Баша).
Список всех доступных команд: /help""", update["message"]["chat"]["id"])

            elif re.search('(умеешь)|(help)|(command)|(помощь)|(команд)|(возможност)', str(text), re.IGNORECASE):
                send_message("""Список всех команд, известных боту:
Шутка с ithappens: (ithumor)|(пошути)|(шуткани)
Баян с bash: (bayan)|(баян)|(баш)|(история)
Хороший фильм: (film)|(кинопоиск)
Трендовый фильм с IMDb: (imdb)|(фильм)|(что посмотреть)|(кино)
Статья дня с Вики (допилю, что отправлялась автоматом): (статья вики)|(вики статья)
Картинка дня с Вики (тоже допилю): (картинка вики)|(вики картинка)
Включить клавиатуру: /getkeyb
Выключить клавиатуру: /removekeyb
                """, update["message"]["chat"]["id"])

            elif re.search('/start', text, re.IGNORECASE):
                send_keyb_message("""Здравстуйте! Вас приветствует ЕА Столовый Бот. Для начала работы отправьте ваш контакт.""", '{"one_time_keyboard":true,"keyboard":[[{"text":"Отправить свой контакт боту","request_contact":true}],["Не отправлять"]]}', update["message"]["chat"]["id"])

            elif re.search('/getkeyb', text, re.IGNORECASE):
                send_keyb_message("""Клавиатура включена. Для удаления введите: /removekeyb""", '{"keyboard":[["баш","ithumor"],["film","imdb"],["вики статья"],["вики картинка"]]}', update["message"]["chat"]["id"])

            elif re.search('/removekeyb', text, re.IGNORECASE):
                send_keyb_message("""Клавиатура удалена. Для восстановления введите: /getkeyb""", '{"remove_keyboard":true}', update["message"]["chat"]["id"])

            elif re.search('кого любит андрей', text, re.IGNORECASE):
                send_message("Настю!", update["message"]["chat"]["id"])

            elif re.search('(ithumor)|(пошути)|(шуткани)', text, re.IGNORECASE):
                send_typing(update["message"]["chat"]["id"])
                send_message(shutka_ithappens(), update["message"]["chat"]["id"])

            elif re.search('(bayan)|(баян)|(баш)|(история)', text, re.IGNORECASE):
                send_typing(update["message"]["chat"]["id"])
                send_message(shutka_bash(), update["message"]["chat"]["id"])

            elif re.search('(film)|(кинопоиск)', text, re.IGNORECASE):
                send_typing(update["message"]["chat"]["id"])
                send_message(good_film_kinopoisk(), update["message"]["chat"]["id"])

            elif re.search('(imdb)|(фильм)|(что посмотреть)|(кино)', text, re.IGNORECASE):
                send_typing(update["message"]["chat"]["id"])
                send_message(good_film_imdb(), update["message"]["chat"]["id"])

            elif re.search('(статья вики)|(вики статья)', text, re.IGNORECASE):
                send_typing(update["message"]["chat"]["id"])
                send_message(wiki_stat_oftheday(), update["message"]["chat"]["id"])

            elif re.search('(картинка вики)|(вики картинка)', text, re.IGNORECASE):
                send_typing(update["message"]["chat"]["id"])
                send_photo(wiki_pic_oftheday()[0], wiki_pic_oftheday()[1], update["message"]["chat"]["id"])

            elif re.search('/getstolkeyb', text, re.IGNORECASE):
                send_keyb_message("""Клавиатура-меню включена. Для отключения введите: /removekeyb""", '{"keyboard":[["/первое","/второе","/гарнир"],["/напиток","/салат","/выпечка"],["/сброс","/готово"]]}', update["message"]["chat"]["id"])

            elif re.search('(/первое)|(/второе)|(/гарнир)|(/напиток)|(/салат)|(/выпечка)', text, re.IGNORECASE):
                chatid = str(update["message"]["chat"]["id"])
                eastol_zakaz(chatid)
я лю
эээээ
я люблю тебя!!!
ура
я тебя тоже
м:ур* мур:*
:****
<3
            else:
                send_message(('+ ' + str(text) + ' +'), update["message"]["chat"]["id"])

            message_was_sent = 1
        except:
            passблю теб
            print(e.message)






        if message_was_sent == 0:
            send_message("Ошибка при попытке ответить на сообщение(((", update["message"]["chat"]["id"])

        time.sleep(1)






def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=HTML".format(text, chat_id)
    get_url(url)

def send_keyb_message(text, rep_markup, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&reply_markup={}&chat_id={}".format(text, rep_markup, chat_id)
    get_url(url)

def send_typing(chat_id):
    url = URL + "sendChatAction?chat_id={}&action=typing".format(chat_id)
    get_url(url)


# главный скрипт
def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        try:
            if len(updates["result"]) > 0:
                last_update_id = get_last_update_id(updates) + 1
                echo_all(updates)
            time.sleep(1)
        except:
            print('ОШИПКО!!! --KeyError: result???--')
            pass




def eastol_zakaz(sdf):
    send_message(('+ ' + str(sdf) + ' +'), update["message"]["chat"]["id"])








################## СТАРТ БОТА
print(':DDDDD SUTATO! Бот начал работу ---> ' + str(datetime.datetime.now()))

if __name__ == '__main__':
    main()


























########## для дебага
#print(requests.get('https://api.telegram.org/bot652844002:AAFPHFs48zVNiEoNv9Yp1rpp4l2fmBjOZ20/sendPhoto?chat_id=292397556&photo=' + picoftheday_pic + '&caption=' + picoftheday_text))




#print(requests.get('https://api.telegram.org/bot652844002:AAFPHFs48zVNiEoNv9Yp1rpp4l2fmBjOZ20/sendPhoto?chat_id=292397556&photo=' + picoftheday_pic + '&caption=' + picoftheday_text))


#https://api.telegram.org/bot652844002:AAFPHFs48zVNiEoNv9Yp1rpp4l2fmBjOZ20/sendChatAction?chat_id=292397556&action=typing
