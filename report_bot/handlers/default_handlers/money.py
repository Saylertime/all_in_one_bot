from loader import bot
from telebot.types import Message
from states.overall import OverallState
from utils.sheets import rep_month

@bot.message_handler(commands=['money'])
def money(message: Message) -> None:

    bot.send_message(message.chat.id, "Введи месяц и год в формате 'Январь 2024'")
    bot.set_state(message.from_user.id, OverallState.second)

@bot.message_handler(state=OverallState.second)
def answer(message):
    msg = rep_month(message.text)
    bot.send_message(message.chat.id, msg)
    bot.delete_state(message.chat.id)
