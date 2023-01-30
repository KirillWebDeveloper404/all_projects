from aiogram.dispatcher.filters.state import StatesGroup, State


class AddNewCategoryClub(StatesGroup):
    name = State()