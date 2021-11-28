from aiogram.dispatcher.filters.state import State, StatesGroup


class fill_up(StatesGroup):
    photo = State()
    test_photo = State()
    name = State()
    course = State()


class memorize(StatesGroup):
    memorize_course = State()
    answer = State()
