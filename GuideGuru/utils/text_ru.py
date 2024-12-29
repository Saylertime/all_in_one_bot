import aiohttp
import asyncio
import json
from config_data import config


async def text_unique_check(text):
    try:
        URL = "https://api.text.ru/post"
        request = {"userkey": config.USERKEY_TEXT_RU, "text": text}

        async with aiohttp.ClientSession() as session:
            async with session.post(URL, data=request) as response:
                if response.status != 200:
                    return f"Ошибка при обращении к API. Status code: {response.status}"

                response_text = await response.text()
                if not response_text:
                    return "Пустой ответ от API"

        try:
            response_data = json.loads(response_text)
        except json.JSONDecodeError:
            with open("error.txt", "a") as file:
                file.write(str(response_text))
            return "Ошибка: Ответ не в формате JSON"

        text_uid = response_data.get("text_uid")
        if not text_uid:
            return "Ошибка: Не удалось получить text_uid"

        print(response_data)
        print(text_uid)

        second_request = {
            "userkey": config.USERKEY_TEXT_RU,
            "uid": text_uid,
            "jsonvisible": "detail",
        }

        second_response = None
        while True:
            async with aiohttp.ClientSession() as session:
                async with session.post(URL, data=second_request) as response:
                    second_response = await response.json()

            if second_response.get("error_desc") != "Текст ещё не проверен":
                print("Готово")
                break

            print("Ещё раз")
            await asyncio.sleep(10)

        unique = second_response.get("text_unique")
        result_json_dict = json.loads(second_response["result_json"])
        urls = result_json_dict.get("urls", [])
        url_keys = [item.get("url", "") for item in urls]
        url_keys_str = "\n— ".join(url_keys)

        spell_check = result_json_dict.get("spell_check")
        seo_check = json.loads(second_response["seo_check"])
        count_words = seo_check.get("count_words")
        spam_percent = seo_check.get("spam_percent")
        water_percent = seo_check.get("water_percent")
        count_chars_with_space = seo_check.get("count_chars_with_space")
        count_chars_without_space = seo_check.get("count_chars_without_space")

        msg = ""

        msg += (
            f"Уникальность: {unique}\n"
            f"Посмотреть все заимствования на сайте: https://text.ru/antiplagiat/{text_uid}\n"
            f"Количество слов: {count_words}\n"
            f"Количество символов с пробелом: {count_chars_with_space}\n"
            f"Процент спама: {spam_percent if spam_percent else '0'}\n"
            f"Процент воды: {water_percent if water_percent else '0'}\n"
            f"Грамматика: {spell_check if spell_check else 'Вроде бы всё чётко'}\n"
            f"Откуда скопировано: {url_keys_str if url_keys and len(url_keys) < 3333 else 'Вроде, ниоткудова'}"
        )

        print(count_words)
        print(count_chars_with_space)
        print(count_chars_without_space)

        return msg

    except Exception as e:
        return f"Ошибка: {e}"


async def symbols_left():
    try:
        URL = "https://api.text.ru/account"
        request = {"userkey": config.USERKEY_TEXT_RU, "method": "get_packages_info"}

        async with aiohttp.ClientSession() as session:
            async with session.post(URL, data=request) as response:
                if response.status != 200:
                    return "Ошибка при обращении к API"
                response_data = await response.json()
                value = response_data.get("size", "Ошибка")
                msg = "{:,}".format(value)
                return msg

    except Exception as e:
        return str(e)
