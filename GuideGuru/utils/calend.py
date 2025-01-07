import calendar
from datetime import datetime, timedelta


def previous_month():
    current_date = datetime.now()
    first_day_of_current_month = datetime(current_date.year, current_date.month, 1)
    last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
    previous_month_name = calendar.month_name[last_day_of_previous_month.month]
    previous_month_year = last_day_of_previous_month.year
    month = f"{months_dict[previous_month_name]} {previous_month_year}"
    return month


def next_month():
    current_date = datetime.now()
    next_month_date = current_date.replace(day=1) + timedelta(days=32)
    next_month_name = calendar.month_name[next_month_date.month]
    month = f"{months_dict[next_month_name]} {next_month_date.year}"
    return month


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
    "December": "Декабрь",
}


def current_month():
    current_date = datetime.now()
    month_eng = current_date.strftime("%B")
    now = f"{months_dict[month_eng]} {current_date.year}"
    return now


def current_day():
    t = datetime.now()
    today = t.strftime("%d.%m")
    tom = t + timedelta(days=1)
    tomorrow = tom.strftime("%d.%m")
    return today, tomorrow


def history_file(nickname, command):
    with open("history.txt", "a") as file:
        file.write(f"{datetime.now()} — {nickname} — {command}\n\n")
