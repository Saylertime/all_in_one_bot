from telebot.handler_backends import State, StatesGroup

class OverallState(StatesGroup):
    """ Класс со всеми необходимыми состояниями """

    second = State()
    name = State()
    new_author = State()
    stats = State()
    all_texts = State()
    notifications = State()
