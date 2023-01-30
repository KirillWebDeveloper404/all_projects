from aiogram.dispatcher.filters.state import StatesGroup, State


class CreatePrivateClub(StatesGroup):
    chunnel = State()
    name = State()
    change_name = State()
    chat = State()