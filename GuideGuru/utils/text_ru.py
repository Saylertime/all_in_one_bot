import requests
import json
from time import sleep
from config_data import config


def text_unique_check(text):
    try:

        # URL = 'https://api.text.ru/post'
        #
        # request = {
        # 'userkey': f'{config.USERKEY_TEXT_RU}',
        # 'text': text
        # }
        # response = requests.post(f'{URL}', data=request).json()
        # text_uid = response.get('text_uid')
        #
        # print(response)
        # print(text_uid)


        URL = 'https://api.text.ru/post'
        request = {
            'userkey': config.USERKEY_TEXT_RU,
            'text': text
        }
        response = requests.post(URL, data=request)

        if response.status_code != 200:
            return 'Ошибка при обращении к API: ' + response.text

        # Проверяем, если ответ пустой
        if not response.text:
            return 'Пустой ответ от API'

        response_data = response.json()
        text_uid = response_data.get('text_uid')

        print(response_data)
        print(text_uid)

        second_request = {
        'userkey': f'{config.USERKEY_TEXT_RU}',
        'uid': text_uid,
        # 'uid': '65fed5649096f',
        'jsonvisible':'detail'}

        while True:
            second_response = requests.post(f'{URL}', data=second_request).json()
            sleep(3)
            print('Еще раз')
            if not second_response.get('error_desc') == 'Текст ещё не проверен':
                print("Готово")
                break

        unique = second_response.get('text_unique')
        result_json_dict = json.loads(second_response['result_json'])
        urls = result_json_dict.get('urls', [])
        url_keys = [item.get('url', '') for item in urls]
        url_keys_str = "\n— ".join(url_keys)

        spell_check = result_json_dict.get('spell_check')
        seo_check = json.loads(second_response['seo_check'])
        count_words = seo_check.get('count_words')
        spam_percent = seo_check.get('spam_percent')
        water_percent = seo_check.get('water_percent')
        count_chars_with_space = seo_check.get('count_chars_with_space')
        count_chars_without_space = seo_check.get('count_chars_without_space')

        msg = ''

        msg += f"Уникальность: {unique}\n" \
               f"Посмотреть все заимствования на сайте: https://text.ru/antiplagiat/{text_uid}\n" \
               f"Количество слов: {count_words}\n" \
               f"Количество символов с пробелом: {count_chars_with_space}\n" \
               f"Процент спама: {spam_percent if spam_percent else '0'}\n"\
               f"Процент воды: {water_percent if water_percent else '0'}\n"\
               f"Грамматика: {spell_check if spell_check else 'Вроде бы всё чётко'}\n" \
               f"Откуда скопировано: {url_keys_str if url_keys and len(url_keys) < 3333 else 'Вроде, ниоткудова'}"

        print(count_words)
        print(count_chars_with_space)
        print(count_chars_without_space)

        return msg

    except requests.exceptions.RequestException as e:
        return f"{e}"

def symbols_left():
    try:
        URL = 'https://api.text.ru/account'
        request = {
            'userkey': config.USERKEY_TEXT_RU,
            'method': 'get_packages_info'
        }

        response = requests.post(URL, data=request)

        if response.status_code != 200:
            return 'Ошибка при обращении к API'

        value = response.json().get('size', 'Ошибка')
        msg = "{:,}".format(value)
        return msg

    except Exception as e:
        return str(e)
