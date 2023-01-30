from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateMessageAF(StatesGroup):
    get_test = State()
    get_time_send = State()
    get_day_send = State()
    get_interval_time = State()
    get_msg_interval = State()
    get_text_link = State()
    get_link = State()
    get_delete_hour = State()
    get_document = State()
    get_video_note = State()
    get_voice = State()
    get_audio = State()
    get_video = State()
    get_gif = State()
    get_photo = State()
    get_text = State()
    choice = State()