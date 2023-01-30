from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline.create_test.create_results import create_message_result
from keyboard.inline.create_test.get_test import get_tests_result, get_result_test_qs_dt, get_result_test_dt
from loader import dp
from modules.admin.tests.create_test.get_main_message import send_main_message
from states import AddTest


@dp.callback_query_handler(create_message_result.filter(prefix='test'), state=AddTest.create_result)
async def process_get_test(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    keyboard = await get_tests_result(data)
    if not keyboard:
        await call.answer('У вас нет других вопросов')
        return
    await call.message.delete()
    text = 'Выберете вопрос'
    if data['test']:
        text = 'Выберете'
    else:
        await AddTest.get_test.set()

    await call.answer(cache_time=1)
    await call.message.answer(text, reply_markup=keyboard)


@dp.callback_query_handler(get_result_test_qs_dt.filter(), state=AddTest.get_test)
async def process_adding_test(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await call.answer(cache_time=1)
    question_id = callback_data.get('id')
    await state.update_data(data={
        'test': question_id
    })
    data = await state.get_data()
    await AddTest.create_result.set()
    await send_main_message(data=data, message=call.message)


@dp.callback_query_handler(get_result_test_dt.filter(prefix='change'), state=AddTest.create_result)
async def process_get_test(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(data={
        'test': None
    })
    data = await state.get_data()
    keyboard = await get_tests_result(data)
    if not keyboard:
        await call.answer('У вас нет других вопросов')
        await AddTest.create_result.set()
        await send_main_message(data=data, message=call.message, delete=True)
        return
    text = 'Выберете вопрос'
    await AddTest.get_test.set()
    await call.answer(cache_time=1)
    await call.message.answer(text, reply_markup=keyboard)
