# import requests
# from loader import bot
# import os
# import openai
#
# openai.api_key = os.getenv("CHATGPT_API_KEY")
#
# @bot.message_handler(commands=['test'])
# def test(message):
#     bot.send_message(message.chat.id, 'Привет! Я ChatGPT. Просто напиши мне, и я постараюсь ответить.')
#
# @bot.message_handler(func=lambda message: True)
# def handle_text(message):
#     user_input = message.text
#
#     proxy = {
#         'socks5': 'socks5://localhost:8080',
#     }
#
#     response = requests.post(
#        "https://api.openai.com/v1/engines/gpt-3.5-turbo-instruct/completions",
#        headers={"Authorization": f"Bearer {os.getenv('CHATGPT_API_KEY')}"},
#        json={"prompt": user_input, "max_tokens": 2000},
#        proxies=proxy
#     )
#
#     chatgpt_reply = response.json()['choices'][0]['text'].strip()
#
#     bot.send_message(message.chat.id, chatgpt_reply)
