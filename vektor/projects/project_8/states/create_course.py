from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateCourse(StatesGroup):
    name = State()