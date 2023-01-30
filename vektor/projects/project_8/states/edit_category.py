from aiogram.dispatcher.filters.state import StatesGroup, State


class EditCategory(StatesGroup):
    name = State()
