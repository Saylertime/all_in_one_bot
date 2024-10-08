import requests
from config_data import config

def check_text_in_turgenev(text):
    data = {
        "api": "risk",
        "key": config.TURGENEV_API_KEY,
        "text": text,
    }

    response = requests.post("https://turgenev.ashmanov.com/", data=data)
    msg = ""

    link = "https://turgenev.ashmanov.com/?t="

    if response.status_code == 200:
        result = response.json()
        level = result.get('level')
        risk = result.get('risk')
        details = result.get('details')

        frequency_link = details[0].get('link')
        frequency_sum = details[0].get('sum')

        style_link = details[1].get('link')
        style_sum = details[1].get('sum')

        keywords_link = details[2].get('link')
        keywords_sum = details[2].get('sum')

        formality_link = details[3].get('link')
        formality_sum = details[3].get('sum')

        readability_link = details[4].get('link')
        readability_sum = details[4].get('sum')


        msg += (f"Уровень риска: {level}\n"
                f"Баллов набрано: {risk}\n\n"
                f"<a href='{link}{frequency_link}'>Повторы</a>: {frequency_sum} баллов\n"
                f"<a href='{link}{style_link}'>Стилистика</a>: {style_sum} баллов\n"
                f"<a href='{link}{keywords_link}'>Запросы</a>: {keywords_sum} баллов\n"
                f"<a href='{link}{formality_link}'>Водность</a>: {formality_sum} баллов\n"
                f"<a href='{link}{readability_link}'>Удобочитаемость</a>: {readability_sum} баллов\n"
                )

    else:
        print("Ошибка:", response.status_code, response.text)
        msg = f"{response.status_code} — {response.text}"

    return msg
