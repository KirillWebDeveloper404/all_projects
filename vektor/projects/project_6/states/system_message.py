from aiogram.dispatcher.filters.state import StatesGroup, State


class SystemMessage(StatesGroup):
    photo = State()
    text = State()
    link = State()