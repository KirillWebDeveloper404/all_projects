from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline.create_test.all_data import create_result_delete_button
from loader import dp
from modules.admin.tests.create_test.get_main_message import send_main_message
from states import AddTest


@dp.callback_query_handler(create_result_delete_button.filter(), state=AddTest.all_states)
async def delete_something(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=1)
    thing = callback_data.get('prefix')
    if '%%' in thing:
        things = thing.split('%%')
        for th in things:
            await state.update_data(data={
                th: None
            })
    else:
        await state.update_data(data={
            thing: None
        })
    await AddTest.create_result.set()
    data = await state.get_data()
    await send_main_message(message=call.message, delete=True, data=data)