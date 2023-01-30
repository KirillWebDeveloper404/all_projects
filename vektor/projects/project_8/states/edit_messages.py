from aiogram.dispatcher.filters.state import StatesGroup, State


class EditMessages(StatesGroup):
    text_link = State()
    link = State()
    delete = State()
    test = State()
    text = State()
    document = State()
    video_note = State()
    voice = State()
    audio = State()
    video = State()
    gif = State()
    photo = State()
    start = State()
