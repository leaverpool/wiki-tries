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
                send_keyb_message("""Клавиатура-меню включена. Для отключения введите: /removekeyb""", '{"keyboard":[["/первое","/второе","/гарнир"],["/напиток","/салат","/выпечка"],["/сброс","/подтвердить"]]}', update["message"]["chat"]["id"])

            elif re.search('(/первое)|(/второе)|(/гарнир)|(/напиток)|(/салат)|(/выпечка)', text, re.IGNORECASE):
                send_typing(update["message"]["chat"]["id"])
                ## проверяем, есть ли уже запись в сегодняшнем файле, добавляем с нулялми, если нет
                that_user_id = str(update["message"]["chat"]["id"])
                found_today = 0
                with open(r'stol_order_today.csv', newline='', encoding='utf-8') as f:
                    for row in csv.reader(f, dialect='excel-tab'):
                        if row and row[0] == that_user_id:
                            found_today = 1
                            break
                if found_today == 0:
                    with open(r'stol_order_today.csv', 'a', newline='', encoding='utf-8') as f:
                        row = [that_user_id, '0', '0', '0', '0', '0', '0', 'NOTFIXED']
                        csv.writer(f, dialect='excel-tab').writerow(row)

                ## ищем уже точно существующую строку с айди пользователя и прибавляем +1 первое
                new_rows = []
                with open(r'stol_order_today.csv', encoding='utf-8') as f:
                    for row in csv.reader(f, dialect='excel-tab'):
                        new_row = row
                        if row and row[0] == that_user_id and row[7] == 'FIXED':
                            send_message('Сегодняшний заказ уже был зафиксирован. Если зафиксировалось что-то не то, можно поправить: /lastchancefix', update["message"]["chat"]["id"])
                        if row and row[0] == that_user_id and row[7] == 'NOTFIXED':  # ищем строку с айди пользоваетля в сегодняшнем файле
                            if re.search('/первое', text, re.IGNORECASE):
                                new_row = [row[0], int(row[1]) + 1, row[2], row[3], row[4], row[5], row[6], row[7]]
                            elif re.search('/второе', text, re.IGNORECASE):
                                new_row = [row[0], row[1], int(row[2]) + 1, row[3], row[4], row[5], row[6], row[7]]
                            elif re.search('/гарнир', text, re.IGNORECASE):
                                new_row = [row[0], row[1], row[2], int(row[3]) + 1, row[4], row[5], row[6], row[7]]
                            elif re.search('/напиток', text, re.IGNORECASE):
                                new_row = [row[0], row[1], row[2], row[3], int(row[4]) + 1, row[5], row[6], row[7]]
                            elif re.search('/салат', text, re.IGNORECASE):
                                new_row = [row[0], row[1], row[2], row[3], row[4], int(row[5]) + 1, row[6], row[7]]
                            elif re.search('/выпечка', text, re.IGNORECASE):
                                new_row = [row[0], row[1], row[2], row[3], row[4], row[5], int(row[6]) + 1, row[7]]
                            # отправляем сообщение с обновлённым общим списком того, что пользователь взял
                            send_message(('Вы взяли:\n<code>Первое: ' + str(new_row[1]) + '  Второе:  ' + str(new_row[2]) + '\nГарнир: ' + str(new_row[3]) + '  Напиток: ' + str(new_row[4]) + '\nСалат:  ' + str(new_row[5]) + '  Выпечка: ' + str(new_row[6]) + '</code>'), update["message"]["chat"]["id"])
                        new_rows.append(new_row)  # add the modified rows
                # overwrite old shit with new temp shit
                with open(r'stol_order_today.csv', 'w', newline='', encoding='utf-8') as f:
                    for row in new_rows:
                        csv.writer(f, dialect='excel-tab').writerow(row)

            elif re.search('(/сброс)|(/подтвердить)|(/lastchancefix)', text, re.IGNORECASE):
                new_rows = []
                send_typing(update["message"]["chat"]["id"])
                that_user_id = str(update["message"]["chat"]["id"])
                with open(r'stol_order_today.csv', encoding='utf-8') as f:
                    for row in csv.reader(f, dialect='excel-tab'):
                        new_row = row
                        if row and row[0] == that_user_id and row[7] == 'FIXED' and re.search('/сброс', text, re.IGNORECASE):
                            send_message('Какой же сброс, когда сегодняшний заказ уже зафиксирован? Если зафиксировалось что-то не то, можно поправить: /lastchancefix', update["message"]["chat"]["id"])
                        if row and row[0] == that_user_id and row[7] == 'NOTFIXED':  # ищем строку с айди пользоваетля в сегодняшнем файле
                            if re.search('/сброс', text, re.IGNORECASE):
                                new_row = [that_user_id, '0', '0', '0', '0', '0', '0', 'NOTFIXED']
                                send_message('Количество обнулено, можно вводить заново.', update["message"]["chat"]["id"])
                            elif re.search('/подтвердить', text, re.IGNORECASE):
                                if row == [that_user_id, '0', '0', '0', '0', '0', '0', 'NOTFIXED']:
                                    send_message('Вы ещё ничего не заказали...', update["message"]["chat"]["id"])
                                else:
                                    new_row = [row[0], row[1], row[2], row[3], row[4], row[5], row[6], 'FIXED']
                                    send_message('Сегодняшний заказ зафиксирован. Приятного аппетита :)', update["message"]["chat"]["id"])
                            # отправляем сообщение с обновлённым общим списком того, что пользователь взял
                        elif row and row[0] == that_user_id and row[7] == 'FIXED':  # ищем строку с айди пользоваетля в сегодняшнем файле
                            if re.search('/lastchancefix', text, re.IGNORECASE):
                                new_row = [that_user_id, '0', '0', '0', '0', '0', '0', 'NOTFIXED']
                                send_message('Сегодняшний подтверждённый заказ удалён! Если Вы сегодня что-то ели, то внесите заново!', update["message"]["chat"]["id"])
                        new_rows.append(new_row)  # add the modified rows
                # overwrite old shit with new temp shit
                with open(r'stol_order_today.csv', 'w', newline='', encoding='utf-8') as f:
                    for row in new_rows:
                        csv.writer(f, dialect='excel-tab').writerow(row)


            else:
                send_message(('+ ' + str(text) + ' +'), update["message"]["chat"]["id"])

            message_was_sent = 1
        except:
            print('ERRRRROOOORRR!!!')
            print(e.__doc__)
            print(e.message)


        try:  # пробуем поймать CONTACT из входящего сообщения и запихнуть в нашу базу, если ещё нет
            contact = update["message"]["contact"]

            print(str(datetime.datetime.now()) + ': ' + str(contact))  # 2018-10-29 20:46:15.614076: {'phone_number': '+79046139180', 'first_name': 'Андрей', 'last_name': 'Левчук', 'user_id': 292397556}
            if re.search('(phone_number)|(first_name)', str(contact), re.IGNORECASE):
                if str(contact.get("user_id")) == str(update["message"]["chat"]["id"]):
                    send_message("О, так это же ваш контакт:", update["message"]["chat"]["id"])
                else:
                    send_message("Нужен именно ваш контакт, а вы прислали чужой:", update["message"]["chat"]["id"])
                send_message(('Вот, что вы прислали:' + '\nНомер телефона: ' + str(contact.get("phone_number")) + '\nИмя: ' + str(contact.get("first_name")) + '\nФамилия: ' + str(contact.get("last_name")) + '\nUSER_ID: ' + str(contact.get("user_id"))), update["message"]["chat"]["id"])
                if str(contact.get("user_id")) == str(update["message"]["chat"]["id"]):
                    send_message("Сейчас поищем ваши данные в базе по USER_ID...", update["message"]["chat"]["id"])
                    found_cont = 0
                    with open(r'contacts.csv', newline='', encoding='utf-8') as f:
                        reader = csv.reader(f, dialect='excel-tab')
                        for row in reader:
                            if row[3] == str(contact.get("user_id")):
                                found_cont = 1
                                send_message(('Вы найдены в базе как:' + '\nНомер телефона: ' + str(row[0]) + '\nИмя: ' + str(row[1]) + '\nФамилия: ' + str(row[2]) + '\nUSER_ID: ' + str(row[3])), update["message"]["chat"]["id"])
                    if found_cont == 0:
                        send_message("Вы не были надены в базе данных, сейчас добавим...", update["message"]["chat"]["id"])
                        with open(r'contacts.csv', 'a', newline='', encoding='utf-8') as f:  # 'a' - append - добавляем, 'w' - заменяем
                            writer = csv.writer(f, dialect='excel-tab')
                            writer.writerow([str(contact.get("phone_number")), str(contact.get("first_name")), str(contact.get("last_name")), str(contact.get("user_id"))])
                        with open(r'contacts.csv', newline='', encoding='utf-8') as f:
                            reader = csv.reader(f, dialect='excel-tab')
                            for row in reader:
                                if row[3] == str(contact.get("user_id")):
                                    send_message(('Готово! Вы занесены в базу как:' + '\nНомер телефона: ' + str(row[0]) + '\nИмя: ' + str(row[1]) + '\nФамилия: ' + str(row[2]) + '\nUSER_ID: ' + str(row[3])), update["message"]["chat"]["id"])

            message_was_sent = 1
        except:
            pass



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

def send_photo(photo, text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendPhoto?photo={}&caption={}&chat_id={}&parse_mode=HTML".format(photo, text, chat_id)
    get_url(url)













# главный скрипт
def main():
    last_update_id = None
    while True:
        try:
            updates = get_updates(last_update_id)
            if len(updates["result"]) > 0:
                last_update_id = get_last_update_id(updates) + 1
                echo_all(updates)
            time.sleep(1)
        except:
            print('Какая-то ошибка главного скрипта')
            pass















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

        # ищем текст picoftheday_text
        picoftheday_text_with_hrefs = content.find_all(class_='main-box-imageCaption')
        picoftheday_text_with_hrefs = str(picoftheday_text_with_hrefs[0])
        picoftheday_text_with_hrefs = (''.join(BeautifulSoup(picoftheday_text_with_hrefs, "html5lib").findAll(text=True)))
        picoftheday_text_with_hrefs = picoftheday_text_with_hrefs.replace("[d]", "")

        return picoftheday_pic, picoftheday_text_with_hrefs










################## СТАРТ БОТА
print(':DDDDD SUTATO! Бот начал работу ---> ' + str(datetime.datetime.now()))

if __name__ == '__main__':
    main()


























########## для дебага
#print(requests.get('https://api.telegram.org/bot652844002:AAFPHFs48zVNiEoNv9Yp1rpp4l2fmBjOZ20/sendPhoto?chat_id=292397556&photo=' + picoftheday_pic + '&caption=' + picoftheday_text))




#print(requests.get('https://api.telegram.org/bot652844002:AAFPHFs48zVNiEoNv9Yp1rpp4l2fmBjOZ20/sendPhoto?chat_id=292397556&photo=' + picoftheday_pic + '&caption=' + picoftheday_text))


#https://api.telegram.org/bot652844002:AAFPHFs48zVNiEoNv9Yp1rpp4l2fmBjOZ20/sendChatAction?chat_id=292397556&action=typing
