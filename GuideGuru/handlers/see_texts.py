from aiogram import Router, F

from config_data import config
from filters.is_author import IsAuthorFilter
from states.overall import OverallState
from datetime import datetime, timedelta
from aiogram_calendar import DialogCalendar, DialogCalendarCallback


router_see_texts = Router()
admins = config.ADMINS


months = {
    "01": "января", "02": "февраля", "03": "марта", "04": "апреля",
    "05": "мая", "06": "июня", "07": "июля", "08": "августа",
    "09": "сентября", "10": "октября", "11": "ноября", "12": "декабря"
}

def format_line(line):
    parts = line.strip().split(" ", 2)
    if len(parts) < 3:
        return line

    date_str, time_str, rest = parts
    dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S.%f")

    formatted = f"{dt.day} {months[dt.strftime('%m')]} {dt.strftime('%H:%M')} {rest}"
    return formatted


async def texts_of_the_day(dates):
    result = []

    with open("texts.txt", "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            for date in dates:
                selected_date_str = date.strftime("%Y-%m-%d")
                if line.startswith(selected_date_str):
                    result.append(format_line(line))
    return result


@router_see_texts.callback_query(F.data == "see_texts_one_day")
async def see_texts_one_day(call, state):
    await state.set_state(OverallState.see_texts)
    await call.message.answer(
        "Выбери дату",
        reply_markup=await DialogCalendar().start_calendar(
            year=datetime.now().year, month=datetime.now().month
        ),
    )


@router_see_texts.callback_query(F.data == "see_texts_period")
async def start_period(call, state):
    await state.set_state(OverallState.see_texts)
    await state.update_data(stage="start")
    await call.message.answer(
        "Выбери дату начала отслеживания",
        reply_markup=await DialogCalendar().start_calendar(
            year=datetime.now().year, month=datetime.now().month
        ),
    )


async def end_period(call, state):
    await state.update_data(stage="end")
    await call.message.answer(
        "Выбери дату конца отслеживания",
        reply_markup=await DialogCalendar().start_calendar(
            year=datetime.now().year, month=datetime.now().month
        ),
    )


@router_see_texts.callback_query(DialogCalendarCallback.filter())
async def process_dialog_calendar(callback_query, callback_data, state):
    stage = (await state.get_data()).get("stage", "")
    selected, date = await DialogCalendar().process_selection(
        callback_query, callback_data
    )

    if not selected:
        return

    if stage == "start":
        await state.update_data(start=date.strftime("%Y-%m-%d"))
        await end_period(callback_query, state)
        return

    if stage == "end":
        await state.update_data(end=date.strftime("%Y-%m-%d"))
        data = await state.get_data()

        start_date = datetime.strptime(data["start"], "%Y-%m-%d").date()
        end_date = datetime.strptime(data["end"], "%Y-%m-%d").date()

        dates = [
            (start_date + timedelta(days=i))
            for i in range((end_date - start_date).days + 1)
        ]
    else:
        dates = [date]

    lines = await texts_of_the_day(dates)

    if lines:
        msg = ""
        for line in lines:
            formatted = f"{line}\n\n"
            if len(msg) + len(formatted) > 4000:
                await callback_query.message.answer(msg)
                msg = ""
            msg += formatted
        if msg:
            await callback_query.message.answer(msg)
    else:
        await callback_query.message.answer("Нет текстов за выбранную дату.")
