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
        text = update["message"]["text"]
        print(str(datetime.datetime.now()) + ': ' + text)

        if str(text) == "123":
            send_message("циферки!", update["message"]["chat"]["id"])

        elif re.search('(прив)|(хэй)|(здрав)|(добрый)|(hi)|(hello)', text, re.IGNORECASE):
            send_message("""Привет! Это тестовый бот, но он уже кое-что умеет (например, постить баяны с Баша).
Список всех доступных команд: /help""", update["message"]["chat"]["id"])

        elif re.search('(умеешь)|(help)|(command)|(помощь)|(команд)|(возможност)', text, re.IGNORECASE):
            send_message("""Список всех команд, известных боту:
Шутка с ithappens: (ithumor)|(пошути)|(шуткани)
Баян с bash: (bayan)|(баян)|(баш)|(история)
Хороший фильм: (film)|(фильм)|(что посмотреть)|(кино)
Статья дня с Вики (допилю, что отправлялась автоматом): (статья вики)|(вики статья)
Картинка дня с Вики (тоже допилю): (картинка вики)|(вики картинка)
            """, update["message"]["chat"]["id"])

        elif re.search('кого любит андрей', text, re.IGNORECASE):
            send_message("Настю!", update["message"]["chat"]["id"])

        elif re.search('(ithumor)|(пошути)|(шуткани)', text, re.IGNORECASE):
            send_message(shutka_ithappens(), update["message"]["chat"]["id"])

        elif re.search('(bayan)|(баян)|(баш)|(история)', text, re.IGNORECASE):
            send_message(shutka_bash(), update["message"]["chat"]["id"])

        elif re.search('(film)|(кинопоиск)', text, re.IGNORECASE):
            send_message(good_film_kinopoisk(), update["message"]["chat"]["id"])

        elif re.search('(imdb)|(фильм)|(что посмотреть)|(кино)', text, re.IGNORECASE):
            send_message(good_film_imdb(), update["message"]["chat"]["id"])

        elif re.search('(статья вики)|(вики статья)', text, re.IGNORECASE):
            send_message(wiki_stat_oftheday(), update["message"]["chat"]["id"])

        elif re.search('(картинка вики)|(вики картинка)', text, re.IGNORECASE):
            send_photo(wiki_pic_oftheday()[0], wiki_pic_oftheday()[1], update["message"]["chat"]["id"])

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

def shutka_ithappens():
    # парсим итхэппенс и берём случайную хохму
    site = requests.get('https://ithappens.me/random')
    if site.status_code is 200:
        content = BeautifulSoup(site.content, 'html5lib')
        stories = content.find_all(class_='story')
        texts = stories[0].find_all(class_='text')
        text = ''.join(BeautifulSoup(str(texts[0]).replace('</p><p>', '\n'), "html5lib").findAll(text=True))
        return str(text)


def shutka_bash():
    # парсим баш и берём случайный баян
    site = requests.get('https://bash.im/random')
    if site.status_code is 200:
        content = BeautifulSoup(site.content, 'html5lib')
        citates = content.find_all(class_='text')
        text_wow = ''.join(BeautifulSoup(str(citates[0]).replace('<br/>', '\n'), "html5lib").findAll(text=True))
        return str(text_wow)


def good_film_kinopoisk():
    # парсим кинопоиск и берём случайный хороший фильм с 2010 года и с рейтингом не ниже 7.4 (максимум 200 в списке)
    site = requests.get('https://www.kinopoisk.ru/top/navigator/m_act[years]/2010%3A2018/m_act[num_vote]/1005/m_act[rating]/7.4%3A/m_act[tomat_rating]/71%3A/m_act[review_procent]/60%3A/m_act[ex_rating]/7.5%3A/m_act[is_film]/on/order/rating/perpage/200/#results')
    if site.status_code is 200:
        content = BeautifulSoup(site.content, 'html5lib')
        good_films = content.find_all(class_='name')
        chosen_good_film = good_films[random.randint(0, len(good_films))]
        m = re.search('<a href="(\s|\S)*?"', str(chosen_good_film))
        chosen_good_film_url = ('https://www.kinopoisk.ru' + m.group(0)[9:-1])
        chosen_good_film_href = chosen_good_film_url + ' '
        chosen_good_film_text = ' '
        text_message = chosen_good_film_text + chosen_good_film_href
        return text_message


def good_film_imdb():
    # парсим IMDB и берём случайный фильм из сотни сравнительно новых и трендовых
    site = requests.get('https://www.imdb.com/chart/moviemeter?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=4da9d9a5-d299-43f2-9c53-f0efa18182cd&pf_rd_r=KS4GXFQ7P2TBMQ4W7ZRR&pf_rd_s=right-4&pf_rd_t=15506&pf_rd_i=toptv&ref_=chttvtp_ql_2')
    if site.status_code is 200:
        content = BeautifulSoup(site.content, 'html5lib')
        good_films = content.find_all(class_='titleColumn')
        chosen_good_film = good_films[random.randint(0, len(good_films) - 1)]
        m = re.search('<a href="(\s|\S)*?"', str(chosen_good_film))
        chosen_good_film_url = ('https://www.imdb.com' + m.group(0)[9:-1])
        return chosen_good_film_url


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
        content = BeautifulSoup(site.content, 'html5lib')

        # ищем картинку picoftheday_pic_href
        picoftheday_pic = content.find_all(class_='main-box-content')
        picoftheday_pic = re.search('src="(\s|\S)*?\.jpg"', str(picoftheday_pic[0])).group(0)
        picoftheday_pic = ('https:' + picoftheday_pic[5:-1])
        # print(picoftheday_pic)

        # ищем текст picoftheday_text
        picoftheday_text_with_hrefs = content.find_all(class_='main-box-imageCaption')
        picoftheday_text_with_hrefs = str(picoftheday_text_with_hrefs[0])[39:-12]
        picoftheday_text_with_hrefs = picoftheday_text_with_hrefs.replace("/wiki/", "https://ru.wikipedia.org/wiki/")

        print(picoftheday_pic)
        print(picoftheday_text_with_hrefs)

        return picoftheday_pic, picoftheday_text_with_hrefs












################## СТАРТ БОТА
print(':DDDDD SUTATO! Бот начал работу ---> ' + str(datetime.datetime.now()))

if __name__ == '__main__':
    main()


























########## для дебага
#print(requests.get('https://api.telegram.org/bot652844002:AAFPHFs48zVNiEoNv9Yp1rpp4l2fmBjOZ20/sendPhoto?chat_id=292397556&photo=' + picoftheday_pic + '&caption=' + picoftheday_text))


