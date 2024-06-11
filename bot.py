import logging
import os
from datetime import datetime
import json

from telegram.ext import Updater, CommandHandler, MessageHandler, filters

from aggregation import aggregate_data

logging.basicConfig(level=logging.INFO)

TOKEN = '7188357008:AAGXXTiGSV5gQuULD6jF6FtMW_Sf_jpmEPY'

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Привет! Отправьте мне JSON с входными данными.')

def handle_message(update, context):
    try:
        data = json.loads(update.message.text)
        dt_from = datetime.fromisoformat(data['dt_from'])
        dt_upto = datetime.fromisoformat(data['dt_upto'])
        group_type = data['group_type']
        result = aggregate_data(dt_from, dt_upto, group_type)
        context.bot.send_message(chat_id=update.effective_chat.id, text=json.dumps(result, ensure_ascii=False))
    except Exception as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Ошибка: ' + str(e))

import queue

def main():
    updater = Updater(TOKEN)
    logging.info('Бот запущен')
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(MessageHandler(filters.TEXT, handle_message))
    updater.start_polling()
    updater.idle()