# from queue import Queue
# from threading import Thread

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import CommandHandler, MessageHandler, Updater, Filters, CallbackQueryHandler

import logging
import datetime

# HTTP/HTPPS for human https://pypi.org/project/requests/
import requests
from threading import Timer

# importing config
import config

# modules for fetcing info
import http.client
import json

API_ROOT_URL = "http://api.football-data.org/v2"

# setting environmental variable
import os
os.environ["FOOTBALL_DATA_API"] = config.apitoken

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# API interaction branch
def fetch_stats(competition):
    url = '/v2/competitions/' + competition + "/standings"

    connection = http.client.HTTPConnection('api.football-data.org')
    headers = { 'X-Auth-Token': config. apitoken }
    connection.request('GET', url, None, headers)
    response = json.loads(connection.getresponse().read().decode())

    results = []

    standings = response["standings"]

    for standing in standings:
        if(standing["type"] == "TOTAL"):
            rows = standing["table"]
            if(competition == "2001"):
                grp = "\n" + standing["group"]
                results.append(grp)
            for element in rows:
                row = str(element["position"]) + ". " + element["team"]["name"] +"\nP "+ str(element["playedGames"]) + " " + "W " + str(element["won"]) + " " + "D " + str(element["draw"]) + " " + "L " + str(element["lost"]) + " " + "Pts " + str(element["points"]) + " " + "GF " + str(element["goalsFor"]) + " " + "GA " + str(element["goalsAgainst"])
                results.append(row)
    
    seperator = "\n\n"
    value = seperator.join(results);
    if (value == ''):
        value = "Ничего не найдено"
    
    return value

def fetch_today():
    url = '/v2/matches'

    connection = http.client.HTTPConnection('api.football-data.org')
    headers = { 'X-Auth-Token': config. apitoken }
    connection.request('GET', url, None, headers )
    response = json.loads(connection.getresponse().read().decode())

    results = []

    if response["count"] > 0:
        matches = response["matches"]
        for element in matches:
            match = element["homeTeam"]["name"] + " vs " + element["awayTeam"]["name"] + "\n Время - " + element["utcDate"][12:-1]
            results.append(match)
    
    seperator = "\n\n"
    value = seperator.join(results);
    if (value == ''):
        value = "Сегодня нет матчей"
    
    return value

def fetch_live(competition):
    url = '/v2/competitions/' + competition + "/matches?status=LIVE"

    connection = http.client.HTTPConnection('api.football-data.org')
    headers = { 'X-Auth-Token': config.apitoken }
    connection.request('GET', url, None, headers )
    response = json.loads(connection.getresponse().read().decode())

    results = []

    if response["count"] > 0:
        matches = response["matches"]
        for element in matches:
            match = element["homeTeam"]["name"] + "vs" + element["awayTeam"]["name"] + "\n " + element["score"]["fullTime"]["homeTeam"] + " - " + element["score"]["fullTime"]["awayTeam"]

            results.append(match)
    
    seperator = "\n\n"
    value = seperator.join(results);
    if (value == ''):
        value = "Нет идущих LIVE матчей"
    
    return value

def fetch_fixtures(competition):
    current_date = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    tminus10 = str(datetime.datetime.strptime(str(current_date), "%Y-%m-%d") + datetime.timedelta(days=-10))[:10]
    tplus10 = str(datetime.datetime.strptime(str(current_date), "%Y-%m-%d") + datetime.timedelta(days=10))[:10]

    url = API_ROOT_URL + '/competitions/' + competition + "/matches"
    headers = { 'X-Auth-Token': config.apitoken }
    payload = {'dateFrom': tminus10, 'dateTo': tplus10}
    r = requests.get(url, params=payload, headers=headers)
    response = r.json()

    results = []

    if response["count"] > 0:
        matches = response["matches"]
        for element in matches:
            match = element["homeTeam"]["name"] + " vs " + element["awayTeam"]["name"]

            if (element["score"]["fullTime"]["homeTeam"] != ''):
                match += "\n " + str(element["score"]["fullTime"]["homeTeam"]) + " - " + str(element["score"]["fullTime"]["awayTeam"])

            results.append(match)
    
    seperator = "\n\n"
    value = seperator.join(results);
    if (value == ''):
        value = "Нет данных"
    
    return value


# Bot branch
def start(bot, update):

    #Вывести сообщение, когда отправлена команда /start. Обычно это приветственное сообщение
    # update.message.reply_text('Welcome to the Test Bot! I will reply you what you will write me.')
    update.message.reply_text("""Добро пожаловать, """ + update.message.from_user.first_name + """!\n""" 
                              + """Доступные команды:\n"""
                              + """- /football  : Информация о футболе\n"""
                              + """- /live      : LIVE матчи\n"""
                              + """- /results   : Результаты матчей\n"""
                              + """- /standings : Статистика комманд\n"""
                              + """- /today     : Матчи на сегодня\n"""
                              + """[https://vk.com/uefanews](URL)"""
                              , parse_mode="Markdown")
                        
def football(bot, update):
    keyboardButtons = [[InlineKeyboardButton("BAR", url="numl.org/ebc")],
                       [InlineKeyboardButton("Трансляции", url="https://www.soccerstand.com/ru/")],
                       [InlineKeyboardButton("ЛЕ", url="numl.org/ebe")],
                       [InlineKeyboardButton("ЛЧ", url="https://clck.ru/EgJi3")],
                       [InlineKeyboardButton("Футбольные гимны", url="numl.org/ebN")],
                      [InlineKeyboardButton("Олимп", url="https://olimp.kz/")]]

    keyboard = InlineKeyboardMarkup(keyboardButtons)

    #Вывести сообщение, когда отправлена команда /football.
    update.message.reply_text('Поможем найти все про футбол и даже больше.\n' + 'Что вам угодно?:', reply_markup=keyboard)

def today(bot, update):

    #Вывести сообщение, когда отправлена команда /live
    update.message.reply_text('Сегодняшние матчи:\n\n {}'.format(fetch_today()))

def live(bot, update):
    keyboardButtons = [[InlineKeyboardButton("Serie A", callback_data="live_2019")],
                        [InlineKeyboardButton("La Liga", callback_data="live_2014")],
                        [InlineKeyboardButton("Premier League", callback_data="live_2021")],
                        [InlineKeyboardButton("Champions League", callback_data="live_2001")],
                        [InlineKeyboardButton("Exit", callback_data="exit")]]

    keyboard = InlineKeyboardMarkup(keyboardButtons)

    #Вывести сообщение, когда отправлена команда /live
    update.message.reply_text('Выберите соревнавание:\n', reply_markup=keyboard)

def results(bot, update):
    
    keyboardButtons = [[InlineKeyboardButton("Serie A", callback_data="res_2019")],
                        [InlineKeyboardButton("La Liga", callback_data="res_2014")],
                        [InlineKeyboardButton("Premier League", callback_data="res_2021")],
                        [InlineKeyboardButton("Champions League", callback_data="res_2001")],
                        [InlineKeyboardButton("Exit", callback_data="exit")]]

    keyboard = InlineKeyboardMarkup(keyboardButtons)

    #Вывести сообщение, когда отправлена команда /live
    update.message.reply_text('Выберите соревнавание:\n', reply_markup=keyboard)
    
def standings(bot, update):

    keyboardButtons = [[InlineKeyboardButton("Serie A", callback_data="stat_2019")],
                        [InlineKeyboardButton("La Liga", callback_data="stat_2014")],
                        [InlineKeyboardButton("Premier League", callback_data="stat_2021")],
                        [InlineKeyboardButton("Champions League", callback_data="stat_2001")],
                        [InlineKeyboardButton("Exit", callback_data="exit")]]

    keyboard = InlineKeyboardMarkup(keyboardButtons)

    #Вывести сообщение, когда отправлена команда /live
    update.message.reply_text('Выберите соревнавание:\n', reply_markup=keyboard)

# callbacks handler
def button(bot, update):
    query = update.callback_query

    text = "No data"

    if query.data == "1":
        text = "Вы можете использовать какое-либо из данных действий: +, -, /, *"
    elif query.data == "2":
        text = "3+4, 44-12, 43/2, 12*90"
    elif query.data == "exit":
        text = "Hasta la vista, baby!"
    elif query.data[:5] == "live_":
        competition = query.data[5:]
        if(competition == "2001"):
            text = "\t\t\tUEFA Champions League\n\n"
        elif(competition == "2021"):
            text = "\t\t\tEnglish Premier League\n\n"
        elif(competition == "2019"):
            text = "\t\t\tItalian Seria A\n\n"
        elif(competition == "2014"):
            text = "\t\t\tLa Liga\n\n"
        text += fetch_live(competition)
    elif query.data[:4] == "res_":
        competition = query.data[4:]
        if(competition == "2001"):
            text = "\t\t\tUEFA Champions League\n\n"
        elif(competition == "2021"):
            text = "\t\t\tEnglish Premier League\n\n"
        elif(competition == "2019"):
            text = "\t\t\tItalian Seria A\n\n"
        elif(competition == "2014"):
            text = "\t\t\tLa Liga\n\n"
        text += fetch_fixtures(competition)
    elif query.data[:5] == "stat_":
        competition = query.data[5:]
        if(competition == "2001"):
            text = "\t\t\tUEFA Champions League\n\n"
        elif(competition == "2021"):
            text = "\t\t\tEnglish Premier League\n\n"
        elif(competition == "2019"):
            text = "\t\t\tItalian Seria A\n\n"
        elif(competition == "2014"):
            text = "\t\t\tLa Liga\n\n"
        text += fetch_stats(competition)        

    query.edit_message_text(text=text)

# Logging errors
def error(bot, update, error):
    # Запись всех ошибок вызванных Updates
    logger.warning('Update "%s" caused error "%s"' % (update, error))

def main():
    # Создаем EventHandler (обработчик событий) и передаем ему токен (ключ) бота.
    updater = Updater(config.token)  

    #bot = updater.bot

    # Объявление диспетчера, чтобы потом зарегистрировать handlers (обработчики)
    dp = updater.dispatcher

    # Отвечает на команду /start в Телеграм
    dp.add_handler(CommandHandler("start", start))  

    # Отвечает на сообщения в Телеграм
    dp.add_handler(MessageHandler(Filters.text, start))

    # Отвечает на команду /mysubs в Телеграм  
    # dp.add_handler(CommandHandler("mysubs", mysubs))

    # Отвечает на команду /football в Телеграм  
    dp.add_handler(CommandHandler("football", football))

    # Отвечает на команду /live в Телеграм  
    dp.add_handler(CommandHandler("live", live))
    
    # Отвечает на команду /results в Телеграм  
    dp.add_handler(CommandHandler("results", results))

    # Отвечает на команду /standings в Телеграм  
    dp.add_handler(CommandHandler("standings", standings))

    # Отвечает на команду /today в Телеграм  
    dp.add_handler(CommandHandler("today", today))

    # Отвечает на callback запросы в Телеграм  
    dp.add_handler(CallbackQueryHandler(button))

    # Запись всех ошибок
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Бот будет работать до тех пор пока вы не нажмете Ctrl-C 
    # или процесс не получит SIGINT, SIGTERM или SIGABRT. 
    # Этот способ должен использоваться в большинстве случаев т.к. start_polling()
    # не блокирующий и остановит бота правильно.
    updater.idle()

# Keeping alive Heroku app by sending requests each 5 minutes
def keepalive():
    r = requests.get('https://football-notifier.herokuapp.com/')
    r.status_code

keep = Timer(600000, keepalive)
keep.start()

if __name__ == '__main__':
    main()