from aiogram.fsm.state import State, StatesGroup


class OverallState(StatesGroup):
    """Класс со всеми необходимыми состояниями"""

    check = State()
    content_watch = State()
    unique = State()
    get_ids = State()
    receipt = State()
    turgenev = State()
    send_text = State()
    see_texts = State()
