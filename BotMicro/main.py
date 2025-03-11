import telebot

bot = telebot.TeleBot('6271780599:AAEV_zB7To_jQLdhxbPA6wKP01pzVOB6xZQ')

@bot.message_handler(commands=['start'])
def start_message(message):
    try:
        bot.send_message(message.chat.id, 'Привет!')
        #код который может вызвать ошибку.
        open("nofile.txt", "r")

    except FileNotFoundError:
        bot.send_message(message.chat.id, "Произошла ошибка, файл не найден.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла непредвиденная ошибка: {e}")

bot.polling(none_stop=True) 

from os import getenv

from deta import Deta

from bot.factory import create_bot, create_dispatcher
from web.factory import create_app

BOT_TOKEN = getenv('6271780599:AAEV_zB7To_jQLdhxbPA6wKP01pzVOB6xZQ')
assert BOT_TOKEN
TOKEN='6271780599:AAEV_zB7To_jQLdhxbPA6wKP01pzVOB6xZQ'

deta = Deta()

bot, webhook_secret = create_bot(BOT_TOKEN)
dispatcher = create_dispatcher(deta)


app = create_app(
    deta,
    bot,
    dispatcher,
    webhook_secret
)
