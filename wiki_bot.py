# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup
from time import sleep

# парсим глагне вики и берём статью дня
site = requests.get('https://ru.wikipedia.org/wiki/Заглавная_страница')
if site.status_code is 200:
    content = BeautifulSoup(site.content, 'html.parser')
    questions = content.find_all(class_='main-box-responsive-image')
    #print(questions[0])

    # СПАРСИЛИ ЗАГОЛОВОК СТАТЬИ И ССЫЛКУ НА НЕЁ
    stat_headline = questions[0].find_all(class_="mw-headline")
    #print(stat_headline)
    m = re.search('<a href(.|\n)*?</a>', str(stat_headline))
    stat_headline = m.group(0)
    #print(stat_headline)
    stat_headline = (stat_headline[:9] + 'https://ru.wikipedia.org' + stat_headline[9:])
    #print(stat_headline)   # <a href="https://ru.wikipedia.org/wiki/%D0%9F%" title="Патент Великобр">Патент Великобр</a>


    # СПАРСИЛИ КАРТИНКУ ДЛЯ СТАТЬИ
    stat_img = questions[0].find_all(class_="floatright")
    #print(stat_img)
    m = re.search('upload.wikimedia.org(\S|\n)*?"', str(stat_img))
    stat_img = m.group(0)[:-1]
    stat_img_href = (stat_img[:0] + '<a href="https://' + stat_img[0:] + '">.</a>')
    stat_img = (stat_img[:0] + 'https://' + stat_img[0:])
    #print(stat_img)         # https://upload.wikimedia.org/wikipedia/commons/thumb/1/Neuma_crop.jpg/200px-Neuma_crop.jpg
    #print(stat_img_href)    # <a href="https://upload.wikimedia.org/wikip.jpg"></a>



    # ПАРСИМ САМ ТЕКСТ СТАТЬИ
    m = re.search('<p><b><a href="(.|\n)*?<div style="clear:both;">', str(questions[0]))
    stat_html_text = m.group(0)
    #print(stat_html_text)
    m = re.search('title=(.|\n)*?<div style="clear:both;">', stat_html_text)
    stat_html_text = m.group(0)
    #print(stat_html_text)
    stat_text = (''.join(BeautifulSoup(stat_html_text, "html.parser").findAll(text=True)))
    #print(stat_text)
    m = re.search('>(.|\s)+', stat_text)
    stat_text = str(m.group(0)[1:])
    #print(stat_text)  # получаем полный текст статьи, который идёт с красной строки, включает название



    #requests.get('https://api.telegram.org/bot652844002:AAFPHFs48zVNiEoNv9Yp1rpp4l2fmBjOZ20/sendPhoto?chat_id=292397556&photo=' + stat_img + '&caption=' + stat_text + ' ' + stat_headline + "&parse_mode=HTML")
    requests.get('https://api.telegram.org/bot652844002:AAFPHFs48zVNiEoNv9Yp1rpp4l2fmBjOZ20/sendMessage?chat_id=292397556&text=qweqwe')






# парсим глагне вики и берём изображение дня
site = requests.get('https://ru.wikipedia.org/wiki/Заглавная_страница')
if site.status_code is 200:
    content = BeautifulSoup(site.content, 'html.parser')
    picoftheday_pic = content.find_all(class_='main-box-content')
    print(picoftheday_pic[0])

    picoftheday_text = content.find_all(class_='main-box-imageCaption')
    print(picoftheday_text[0])