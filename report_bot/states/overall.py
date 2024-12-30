from aiogram.fsm.state import State, StatesGroup


class OverallState(StatesGroup):
    """Класс со всеми необходимыми состояниями"""

    all_texts = State()
    history = State()
    money = State()
    new_author = State()
    stats_month = State()
