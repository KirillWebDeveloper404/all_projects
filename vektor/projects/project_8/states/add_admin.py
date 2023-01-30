from aiogram.dispatcher.filters.state import State, StatesGroup


class AddAdmin(StatesGroup):
    get_admin_id = State()
