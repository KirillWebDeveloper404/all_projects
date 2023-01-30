from aiogram.dispatcher.filters.state import State, StatesGroup


class AddAudio(StatesGroup):
    waiting_for_name = State()
    waiting_for_audio = State()
