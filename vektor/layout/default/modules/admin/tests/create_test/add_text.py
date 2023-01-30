from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline.create_test.create_results import create_message_result
from keyboard.inline.create_test.get_result_text import get_text_result, get_result_text_dt
from loader import dp
from states import AddTest
from .get_main_message import send_main_message


@dp.callback_query_handler(create_message_result.filter(prefix='text'), state=AddTest.create_result)
async def process_get(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    keyboard = await get_text_result(data)
    text = 'Отправьте текст'
    if data['result_text']:
        text = 'Выберете'
    else:
        await AddTest.get_text.set()
    await call.message.delete()
    await call.message.answer(text, reply_markup=keyboard)


@dp.callback_query_handler(get_result_text_dt.filter(prefix='change'), state=AddTest.create_result)
async def process_change(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await AddTest.get_photo.set()
    await state.update_data(data={
        'result_text': None
    })
    data = await state.get_data()
    keyboard = await get_text_result(data)
    await call.message.edit_text('Отправьте текст', reply_markup=keyboard)
    await AddTest.get_text.set()


@dp.message_handler(state=AddTest.get_text)
async def process_add(message: types.Message, state: FSMContext):
    text = message.text
    await state.update_data(data={
        'result_text': text
    })
    data = await state.get_data()
    await AddTest.create_result.set()
    await send_main_message(data=data, message=message)


