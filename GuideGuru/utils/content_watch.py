import requests
from config_data import config

def content_watch_check(text):
    try:
        url = "https://content-watch.ru/public/api/"
        data = {
            "key": "Y1LnHQ0t6b1uUjO",
            "action": "CHECK_TEXT",
            "text": text,
            "test": 0
        }

        response = requests.post(url=url, data=data)
        result = response.json()
        msg = ""

        with open('ttt.txt', 'a') as file:
            file.write(str(response.text))

        if result["error_code"] == 0:
            msg += f"Процент уникальности: {result['percent']}\n\n"
            if len(result["matches"]) > 0:
                for i in result["matches"]:
                    normal_url = i["url"].replace("\\/", "/")
                    msg += f"{i['percent']} процентов — скопировано отсюда: {normal_url}\n"
        else:
            msg = f"ОШИБКА: {result['error']}"

        return msg

    except:
        return "Произошла какая-то ошибка. Напиши @saylertime, он пофиксит (возможно)"
