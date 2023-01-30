from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline.create_test.all_data import create_result_back_button
from loader import dp
from modules.admin.tests.create_test.get_main_message import send_main_message
from states import AddTest


@dp.callback_query_handler(create_result_back_button.filter(), state=AddTest.all_states)
async def back(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    data = await state.get_data()
    await AddTest.create_result.set()
    await send_main_message(data=data, message=call.message, delete=True)