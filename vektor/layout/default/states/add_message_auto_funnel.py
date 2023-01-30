from aiogram.dispatcher.filters.state import StatesGroup, State


class AddMessageFunnel(StatesGroup):
    get_message = State()
    get_link = State()
    get_text_link = State()
    get_photo = State()
    get_document = State()
    get_audio = State()
    get_gif = State()
    get_day = State()
    get_time = State()