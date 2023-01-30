from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline.create_test.create_results import create_message_result
from keyboard.inline.create_test.main_question_kb import main_question_kb, main_question_kb_dt
from keyboard.inline.create_test.main_question_messages import get_main_msg_question
from keyboard.inline.tests.main import test_main
from loader import dp
from modules.admin.tests.create_test.save_result import save_result
from states import AddTest


@dp.callback_query_handler(create_message_result.filter(prefix='save'), state=AddTest.create_result)
async def process_save_answer(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    await save_result(data=data)
    await call.message.delete()
    await state.update_data(data={
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
    text = await get_main_msg_question(data['question_id'])
    await call.message.answer(text, reply_markup=main_question_kb)
    await AddTest.finish.set()


@dp.callback_query_handler(main_question_kb_dt.filter(prefix='add_new'), state=AddTest.finish)
async def process_add_new(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.delete()
    await call.message.answer('Отправьте ответ')
    await AddTest.get_answer.set()


@dp.callback_query_handler(main_question_kb_dt.filter(prefix='close'), state=AddTest.finish)
async def process_close_create_test(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    await call.answer(cache_time=1)
    await call.message.answer('Квизы', reply_markup=test_main)
