from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateRateCourse(StatesGroup):
    month_start = State()
    week_start = State()
    start = State()
    close_time = State()
    demo = State()
    duration = State()
    channel = State()
    chat = State()
    media = State()
    desc = State()
    price = State()
    name = State()
    process = State()