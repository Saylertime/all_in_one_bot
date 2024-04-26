from loader import bot
from utils.sheets import in_work_today

@bot.message_handler(commands=['deadlines'])
def deadlines(message):
    msg = in_work_today()
    bot.send_message(message.chat.id, msg, parse_mode='HTML')