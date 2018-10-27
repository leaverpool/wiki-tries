# -*- encoding: utf-8 -*-
import json
import requests
import time
import urllib
import config
import datetime
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
    #print(str(datetime.datetime.now()) + str(js))

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
        print(str(datetime.datetime.now()) + ': ' + text)

        if str(text) == "123":
            send_message("циферки!", update["message"]["chat"]["id"])

        elif re.search('кого любит андрей', text, re.IGNORECASE):
            send_message("Настю!", update["message"]["chat"]["id"])

        elif re.search('(пошути)|(шуткани)', text, re.IGNORECASE):
            send_message(shutka(), update["message"]["chat"]["id"])

        elif re.search('(статья вики)|(вики статья)', text, re.IGNORECASE):
            send_message(wiki_stat_oftheday(), update["message"]["chat"]["id"])

        elif re.search('(картинка вики)|(вики картинка)', text, re.IGNORECASE):
            send_photo(wiki_pic_oftheday()[0], wiki_pic_oftheday()[1], update["message"]["chat"]["id"])
            #print(wiki_pic_oftheday()[0], wiki_pic_oftheday()[1])

        #chat = update["message"]["chat"]["id"]
        else:
            send_message(str('+ ' + text + ' +'), update["message"]["chat"]["id"])
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

def send_photo(photo, text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendPhoto?photo={}&caption={}&chat_id={}&parse_mode=HTML".format(photo, text, chat_id)
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



def wiki_stat_oftheday():
    # парсим глагне вики и берём статью дня, отправляем в виде текста + картинка href в конце
    site = requests.get('https://ru.wikipedia.org/wiki/Заглавная_страница')
    if site.status_code is 200:
        content = BeautifulSoup(site.content, 'html.parser')
        questions = content.find_all(class_='main-box-responsive-image')

        # СПАРСИЛИ ЗАГОЛОВОК СТАТЬИ И ССЫЛКУ НА НЕЁ
        stat_headline = questions[0].find_all(class_="mw-headline")
        m = re.search('<a href(.|\n)*?</a>', str(stat_headline))
        stat_headline = m.group(0)
        stat_headline = (stat_headline[:9] + 'https://ru.wikipedia.org' + stat_headline[9:])
        # print(stat_headline)   # <a href="https://ru.wikipedia.org/wiki/%D0%9F%" title="Патент Великобр">Патент Великобр</a>

        # СПАРСИЛИ КАРТИНКУ ДЛЯ СТАТЬИ
        stat_img = questions[0].find_all(class_="floatright")
        m = re.search('upload.wikimedia.org(\S|\n)*?"', str(stat_img))
        stat_img = m.group(0)[:-1]
        stat_img_href = (stat_img[:0] + '<a href="https://' + stat_img[0:] + '">.</a>')
        stat_img = (stat_img[:0] + 'https://' + stat_img[0:])
        # print(stat_img_href)    # <a href="https://upload.wikimedia.org/wikip.jpg"></a>
        # print(stat_img)         # https://upload.wikimedia.org/wikipedia/commons/thumb/1/Neuma_crop.jpg/200px-Neuma_crop.jpg

        # ПАРСИМ САМ ТЕКСТ СТАТЬИ
        m = re.search('<p><b><a href="(.|\n)*?<div style="clear:both;">', str(questions[0]))
        stat_html_text = m.group(0)
        # print(stat_html_text)
        m = re.search('title=(.|\n)*?<div style="clear:both;">', stat_html_text)
        stat_html_text = m.group(0)
        # print(stat_html_text)
        stat_text = (''.join(BeautifulSoup(stat_html_text, "html.parser").findAll(text=True)))
        # print(stat_text)
        m = re.search('>(.|\s)+', stat_text)
        stat_text = str(m.group(0)[1:])
        stat_text = stat_text[:-3]  # минус перенос строки, пробел и точка (точка для точки-ссылки)
        # print(stat_text)  # получаем полный текст статьи, который идёт с красной строки, включает название

        output = stat_text + stat_img_href
        return output

def wiki_pic_oftheday():
    # парсим глагне вики и берём изображение дня, постим в виде фотографии + подписи
    site = requests.get('https://ru.wikipedia.org/wiki/Заглавная_страница')
    if site.status_code is 200:
        content = BeautifulSoup(site.content, 'html.parser')

        # ищем картинку picoftheday_pic_href
        picoftheday_pic = content.find_all(class_='main-box-content')
        # print(picoftheday_pic[0])
        m = re.search('src="(\s|\S)*?\.jpg"', str(picoftheday_pic[0]))
        picoftheday_pic = m.group(0)
        # print(picoftheday_pic)
        picoftheday_pic = ('https:' + picoftheday_pic[5:-1])
        picoftheday_pic_href = ('<a href="https:' + picoftheday_pic[5:-1] + '">.</a>')
        # print(picoftheday_pic_href)  # <a href="https://upload.wikimedia.org/wikipedia/commons/thumb/f/fd/Black-headed_lapwing_%28Vanellus_tectus_tectus%29.jpg/500px-Black-headed_lapwing_%28Vanellus_tectus_tectus%29.jpg">.</a>

        # ищем текст picoftheday_text
        picoftheday_text = content.find_all(class_='main-box-imageCaption')
        # print(picoftheday_text[0])
        m = re.search('<a href="(\s|\S)*?"', str(picoftheday_text[0]))
        picoftheday_text = m.group(0)
        # print(picoftheday_text)
        picoftheday_text = ('https://ru.wikipedia.org' + picoftheday_text[9:-1])
        # print(picoftheday_text)  # https://ru.wikipedia.org/wiki/Чибисы
        site = requests.get(picoftheday_text)
        if site.status_code is 200:
            content = BeautifulSoup(site.content, 'html.parser')
            picoftheday_text = content.find_all(class_='mw-parser-output')
            m = re.search('<p><b>(\s|\S)*?</p>', str(picoftheday_text[0]))
            picoftheday_text = m.group(0)
            # print(picoftheday_text)
            picoftheday_text = (''.join(BeautifulSoup(picoftheday_text, "html.parser").findAll(text=True)))
            # picoftheday_text = picoftheday_text[:400]  # обрезаем для сообщения, если есть лимит на кол-во знаков
            # print(picoftheday_text)

        return picoftheday_pic, picoftheday_text
        #print(requests.get('https://api.telegram.org/bot652844002:AAFPHFs48zVNiEoNv9Yp1rpp4l2fmBjOZ20/sendPhoto?chat_id=292397556&photo=' + picoftheday_pic + '&caption=' + picoftheday_text))












################## СТАРТ БОТА
print(':DDDDDDDDDDDDDDDDDD   SUTATO! Бот начал работу --------> ' + str(datetime.datetime.now()))

if __name__ == '__main__':
    main()




