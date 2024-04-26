from datetime import datetime, timedelta

months_dict = {
    "January": "Январь",
    "February": "Февраль",
    "March": "Март",
    "April": "Апрель",
    "May": "Май",
    "June": "Июнь",
    "July": "Июль",
    "August": "Август",
    "September": "Сентябрь",
    "October": "Октябрь",
    "November": "Ноябрь",
    "December": "Декабрь"
}

def current_month():
    current_date = datetime.now()
    month_eng = current_date.strftime("%B")
    now = f"{months_dict[month_eng]} {current_date.year}"
    return now

def current_day():
    t = datetime.now()
    today = t.strftime('%d.%m')
    tom = t + timedelta(days=1)
    tomorrow = tom.strftime('%d.%m')
    return today, tomorrow

