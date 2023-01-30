from aiogram.dispatcher.filters.state import StatesGroup, State


class EditCategoryPRCL(StatesGroup):
    name = State()