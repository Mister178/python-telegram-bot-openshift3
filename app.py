import logging
#from queue import Queue
#from threading import Thread
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import CommandHandler, MessageHandler, Updater, Filters, CallbackQueryHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
TOKEN = '561121201:AAEMcoIuVCBsjyGa6DvxGRiAKTTyoagfjik'


def start(bot, update):
    """Вывести сообщение, когда отправлена команда /start.
    Обычно это приветственное сообщение"""
    """update.message.reply_text('Welcome to the Test Bot! I will reply you what you will write me.')"""
    bot.send_message(chat_id=update.message.chat_id,
                     text='<b>KAZGUU site</b>,<a href="http://kazguu.kz/ru/">KAZGUU</a>', parse_mode=ParseMode.HTML)


def football(bot, update):
    """Вывести сообщение, когда отправлена команда /start.
    Это может быть сообщение о том, что ваш бот может делать и список команд"""

    keyboardButtons = [[InlineKeyboardButton("BAR", url1="numl.org/ebc")],
                       [InlineKeyboardButton("Трансляции", url="https://www.soccerstand.com/ru/")],
                       [InlineKeyboardButton("ЛЕ", url="numl.org/ebe")],
                      [InlineKeyboardButton("ЛЧ", url="https://clck.ru/EgJi3")]]
    keyboard = InlineKeyboardMarkup(keyboardButtons)
    update.message.reply_text('Сделайте выбор:', reply_markup=keyboard)


def button(bot, update):
    query = update.callback_query
    if query.data == "1":
        text = "Вы можете использовать какое-либо из данных действий: +, -, /, *"
    elif query.data == "2":
        text = "3+4, 44-12, 43/2, 12*90"
    bot.editMessageText(text=text, chat_id=query.message.chat_id,
                        message_id=query.message.message_id)

def error(bot, update, error):
    """Запись всех ошибок вызванных Updates."""
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def main():
    updater = Updater(TOKEN)  # Создаем EventHandler (обработчик событий) и передаем ему токен (ключ) бота.
    #bot = updater.bot
    dp = updater.dispatcher  # Объявление диспетчера, чтобы потом зарегистрировать handlers (обработчики)
    dp.add_handler(CommandHandler("start", start))  # Отвечает на команду /start в Телеграм
    dp.add_handler(CommandHandler("football", football))  # Отвечает на команду /help в Телеграм
    dp.add_handler(CallbackQueryHandler(button))


    # Запись всех ошибок
    dp.add_error_handler(error)

    updater.start_polling()  # Start the Bot
    """Бот будет работать до тех пор пока вы не нажмете Ctrl-C
     или процесс не получит SIGINT, SIGTERM или SIGABRT. 
     Этот способ должен использоваться в большинстве случаев т.к. start_polling()
      не блокирующий и остановит бота правильно."""
    updater.idle()


if __name__ == '__main__':
    main()
