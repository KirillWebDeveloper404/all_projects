from aiogram.dispatcher.filters.state import State, StatesGroup


class EveryMailing(StatesGroup):
    init = State()
    get_type = State()
    get_day_of_month = State()
    get_day_of_week = State()
    get_time = State()
    get_text = State()
    get_link = State()
    get_text_link = State()
    get_photo = State()
    get_animation = State()
    get_document = State()
    final = State()