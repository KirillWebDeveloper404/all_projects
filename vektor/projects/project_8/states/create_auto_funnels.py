from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateAutoFunnels(StatesGroup):
    get_do_not_buy = State()
    get_do_buy = State()
    choice = State()
    get_name = State()
    get_when_start = State()
    get_day_on_week = State()
    get_day_on_month = State()
    get_product = State()
    final = State()