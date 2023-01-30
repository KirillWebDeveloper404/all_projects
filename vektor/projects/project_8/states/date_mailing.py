from aiogram.dispatcher.filters.state import State, StatesGroup


class DateMailing(StatesGroup):
    init = State()
    get_date = State()
    get_time = State()
    get_text = State()
    get_link = State()
    get_text_link = State()
    get_photo = State()
    get_animation = State()
    get_document = State()
    final = State()
