from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline import create_message_af, msg_delete_hour_data, \
    generate_get_delete_hour_keyboard, delete_time_data, delete_time_kb
from loader import dp
from states import CreateMessageAF
from .get_main_text import send_main_text


@dp.callback_query_handler(create_message_af.filter(prefix='delete_hour'), state=CreateMessageAF.choice)
async def process_delete_hour(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    data = await state.get_data()
    keyboard = await generate_get_delete_hour_keyboard(data=data)
    await call.message.delete()
    if data['delete_hour'] or data['delete_day'] or data['delete_minute'] or data['delete_second']:
        await call.message.answer('Выберете:', reply_markup=keyboard)
    else:
        text = 'Выберете через сколько сообщение удалится:'
        await call.message.answer(text, reply_markup=delete_time_kb)
        await CreateMessageAF.get_delete_hour.set()


@dp.callback_query_handler(delete_time_data.filter(), state=CreateMessageAF.get_delete_hour)
async def get_delete_hour(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    day = int(callback_data.get('day'))
    hour = int(callback_data.get('hour'))
    minute = int(callback_data.get('minute'))
    second = int(callback_data.get('second'))
    await state.update_data(data={
        'delete_day': day,
        'delete_hour': hour,
        'delete_minute': minute,
        'delete_second': second,
    })
    data = await state.get_data()
    await send_main_text(data, call.message, True)
    await CreateMessageAF.choice.set()


@dp.callback_query_handler(msg_delete_hour_data.filter(prefix='change_delete_hour'), state=CreateMessageAF.choice)
async def process_change_delete_hour(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await state.update_data(data={
        'delete_day': None,
        'delete_hour': None,
        'delete_minute': None,
        'delete_second': None,
    })

    text = 'Выберете через сколько сообщение удалится:'
    await call.message.edit_text(text, reply_markup=delete_time_kb)
    await CreateMessageAF.get_delete_hour.set()
