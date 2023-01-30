from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateNotificationPrivateChat(StatesGroup):
    content = State()