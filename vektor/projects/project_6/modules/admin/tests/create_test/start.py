from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from keyboard.inline.tests.main import test_main_data
from loader import dp
from states import AddTest


@dp.callback_query_handler(test_main_data.filter(prefix='new'))
async def process_start_create_test(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await call.message.edit_text("Отправьте вопрос")
    await state.update_data(data={
        'question_text': None,
        'question_id': None,
        'answer': None,
        'answer_id': None,
        'result_text': None,
        'photo': None,
        'gif': None,
        'video': None,
        'audio': None,
        'voice': None,
        'video_note': None,
        'test': None,
        'document': None,
        'link': None,
        'text_link': None
    })
    await AddTest.get_question.set()
