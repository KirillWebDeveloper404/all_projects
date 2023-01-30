from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateMessagePrCl(StatesGroup):
    category = State()
    create_category = State()
    time = State()
    process = State()
    content = State()