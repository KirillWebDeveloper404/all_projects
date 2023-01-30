from aiogram.dispatcher.filters.state import StatesGroup, State


class RatePrivateClub(StatesGroup):
    media = State()
    period_demo = State()
    period = State()
    desc = State()
    price = State()
    process = State()
    name = State()