import logging
import threading

import telebot
from telebot import apihelper

from bot_user import Botuser
from dbconnector import Dbconnetor
import starting_helper
from notificator import Notificator

logging.basicConfig(
    filename='errors.log',
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
logger = telebot.logger



telebot.logger.setLevel(logging.INFO)
use_proxy = Dbconnetor.get_config_parameter('proxy', 'global')
if use_proxy:
    apihelper.proxy = {'https': 'https://{}'.format(use_proxy)}
TOKEN = Dbconnetor.get_config_parameter('api_token', 'aggr_bot')
bot = telebot.TeleBot(TOKEN, threaded=True)
notificator = Notificator(bot=bot)


@bot.message_handler(commands=['start'])
def handlestart(m):
    user = Botuser(uid=m.chat.id, bot=bot)
    try:
        starting_helper.stating_handler(user=user, message=m)
    except:
        logging.exception(str(m))
        logging.exception('Got exception on main handler')
        user.send_message(message_index="ERROR_MESSAGE")


@bot.message_handler(content_types='text')
def simpletextmessage(m):
    user = Botuser(uid=m.chat.id, bot=bot)
    try:
        starting_helper.text_message_handler(user=user, message=m, bot=bot)
    except:
        logging.exception(str(m))
        logging.exception('Got exception on main handler')
        user.send_message(message_index="ERROR_MESSAGE")


@bot.callback_query_handler(func=lambda call: call.data[:6] == 'reply_')
def test_answer_handler(call):
    user = Botuser(uid=call.message.chat.id, bot=bot)
    try:
        starting_helper.reply_to_request_handler(call=call, user=user, bot=bot)
    except:
        logging.exception(str(call))
        logging.exception('Got exception on main handler')
        user.send_message(message_index="ERROR_MESSAGE")


@bot.callback_query_handler(func=lambda call: call.data == 'send_first_post')
def test_answer_handler(call):
    user = Botuser(uid=call.message.chat.id, bot=bot)
    try:
        starting_helper.first_post_handler(call=call, user=user, bot=bot)
    except:
        logging.exception(str(call))
        logging.exception('Got exception on main handler')
        user.send_message(message_index="ERROR_MESSAGE")


@bot.callback_query_handler(func=lambda call: call.data == 'call_back')
def test_answer_handler(call):
    user = Botuser(uid=call.message.chat.id, bot=bot)
    try:
        starting_helper.call_back_handler(call=call, user=user, bot=bot)
    except:
        logging.exception(str(call))
        logging.exception('Got exception on main handler')
        user.send_message(message_index="ERROR_MESSAGE")


th = threading.Thread(target=notificator.get_active_notifications, args=())
th.start()


bot.polling(none_stop=True)
