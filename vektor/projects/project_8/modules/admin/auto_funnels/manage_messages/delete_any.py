from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline.edit.all_data import delete_something
from loader import dp
from states import EditMessages
from utils.functions.edit_messages_msg import get_text_edit_messages


@dp.callback_query_handler(delete_something.filter(), state=EditMessages.all_states)
async def process_delete_something(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    thing = callback_data.get('prefix')
    if '%%' in thing:
        things = thing.split('%%')
        for i in things:
            await state.update_data(data={
                i: None
            })
    elif thing == 'delete':
        await state.update_data(data={
            'delete_day': None,
            'delete_hour': None,
            'delete_minute': None,
            'delete_second': None,
        })
    else:
        await state.update_data(data={
            thing: None
        })

    await call.answer('Удалено')
    await EditMessages.start.set()
    data = await state.get_data()
    await state.update_data(data=data)
    await get_text_edit_messages(data, call.message, delete=True)