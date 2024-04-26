from loader import bot
import handlers
from telebot.custom_filters import StateFilter
from utils.set_bot_commands import set_default_commands
from config_data import config
import time
import threading
from utils.tasks import send_notifications
from flask import Flask, request
import requests
import telebot


app = Flask(__name__)

WEBHOOK_URL = 'https://glinkin.pro'
BOT_TOKEN = config.BOT_TOKEN
LOCAL_ENV = config.LOCAL_ENV


@app.route('/webhook_report', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return 'ok', 200

def set_webhook():
    response = requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={WEBHOOK_URL}/webhook_report')
    print(response.json())

def webhook_thread():
    while True:
        set_webhook()
        time.sleep(30)


def scheduled_job():
    while True:
        send_notifications()
        time.sleep(60)


if __name__ == "__main__":
    bot.delete_webhook()
    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    thread = threading.Thread(target=scheduled_job)
    thread.start()
    # if LOCAL_ENV:
    #     bot.polling()
    # else:
    set_webhook()
    webhook_thread = threading.Thread(target=webhook_thread)
    webhook_thread.start()
    app.run(host='0.0.0.0', port=5003)

