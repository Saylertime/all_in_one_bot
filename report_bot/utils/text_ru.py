import requests
from config_data import config


def text_unique_check():
    try:
        URL = 'https://api.text.ru/account'

        request = {
        'userkey': f'{config.USERKEY_TEXT_RU}',
        'method': 'get_packages_info'
        }
        response = requests.post(f'{URL}', data=request).json()
        value = response.get('size', 'Ошибка')
        msg = "{:,}".format(value)
        return msg

    except Exception as e:
        msg = str(e)
    return msg
