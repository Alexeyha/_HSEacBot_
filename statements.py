from aiogram.dispatcher.filters.state import State, StatesGroup


class fill_up(StatesGroup):
    password = State()
    photo = State()
    test_photo = State()
    name = State()
    course = State()


class memorize(StatesGroup):
    memorize_course = State()
    answer = State()
