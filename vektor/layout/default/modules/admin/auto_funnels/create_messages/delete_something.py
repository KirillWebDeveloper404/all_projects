from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline.create_message_af.all_data import delete_something
from loader import dp
from states import CreateMessageAF
from .get_main_text import send_main_text


@dp.callback_query_handler(delete_something.filter(), state=CreateMessageAF.choice)
async def process_delete_media(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    thing = callback_data.get('thing')

    if thing == 'delete_timer':
        await state.update_data(data={
            'delete_hour': None,
            'delete_minute': None,
            'delete_second': None,
            'delete_day': None,
        })
    elif thing == 'interval_timer':
        await state.update_data(data={
            'interval_msg': None,
            'interval_hour': None,
            'interval_minute': None,
            'interval_second': None,
            'interval_day': None,
        })
    elif '%%' in thing:
        things = thing.split('%%')
        for x in things:
            await state.update_data(data={
                x: None
            })
    else:
        await state.update_data(data={
            thing: None
        })
    await call.answer(cache_time=1)

    data = await state.get_data()
    await send_main_text(data, call.message, True)
    await CreateMessageAF.choice.set()