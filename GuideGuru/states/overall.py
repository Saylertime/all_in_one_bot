from telebot.handler_backends import State, StatesGroup

class OverallState(StatesGroup):
    """ Класс со всеми необходимыми состояниями """

    check = State()
    unique = State()

class CheckState(StatesGroup):
    """ Класс со всеми необходимыми состояниями """

    check = State()