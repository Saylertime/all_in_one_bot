from loader import bot
from utils.sheets import in_work_today
from utils.logger import logger

@bot.message_handler(commands=['deadlines'])
def deadlines(message):
    logger.warning(f'{message.from_user.username} — команда deadlines')
    msg = in_work_today()
    bot.send_message(message.chat.id, msg, parse_mode='HTML')