from aiogram.dispatcher.filters.state import StatesGroup, State


class AddTest(StatesGroup):
    finish = State()
    get_text = State()
    get_test = State()
    get_text_link = State()
    get_link = State()
    get_document = State()
    get_video_note = State()
    get_voice = State()
    get_audio = State()
    get_video = State()
    get_gif = State()
    get_photo = State()
    create_result = State()
    get_answer = State()
    get_question = State()