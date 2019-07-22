from flask import Flask, request
from telebot.types import Update

from utils.bot_util import bot


app = Flask(__name__)


@app.route('/telegram_web_hook/', methods=['POST'])
def telegram_web_hook():
    update = Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return 'ok', 200
