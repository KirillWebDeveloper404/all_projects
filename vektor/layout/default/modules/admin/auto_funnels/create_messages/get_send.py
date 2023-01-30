from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline import create_message_af, generate_get_msg_send_time_keyboard, msg_send_time_data, \
    get_day_send_msg_kb, day_send_msg_data, time_send_msg_kb, time_send_msg_data
from loader import dp
from .get_main_text import send_main_text
from states import CreateMessageAF


@dp.callback_query_handler(create_message_af.filter(prefix='send'), state=CreateMessageAF.choice)
async def process_adding_send_time(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    data = await state.get_data()
    await call.message.delete()
    if data['day'] and data['hour']:
        keyboard = await generate_get_msg_send_time_keyboard(data=data)
        await call.message.answer('Выберете:', reply_markup=keyboard)
    else:
        text = 'Выберете день:'
        keyboard = await get_day_send_msg_kb(data)
        await call.message.answer(text, reply_markup=keyboard)
        await CreateMessageAF.get_day_send.set()


@dp.callback_query_handler(day_send_msg_data.filter(), state=CreateMessageAF.get_day_send)
async def get_send_time(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    day = int(callback_data.get('day'))

    await state.update_data(data={
        'day': day,
    })
    await call.answer()
    await call.message.edit_text('Выберете время отправки сообщения:', reply_markup=time_send_msg_kb)
    await CreateMessageAF.get_time_send.set()


@dp.callback_query_handler(time_send_msg_data.filter(), state=CreateMessageAF.get_time_send)
async def get_send_time(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    hour = int(callback_data.get('hour'))
    await state.update_data(data={
        'hour': hour,
        'minute': 0,
    })
    await call.answer()
    data = await state.get_data()
    await send_main_text(data, call.message, True)
    await CreateMessageAF.choice.set()


@dp.callback_query_handler(msg_send_time_data.filter(prefix='change_send_time'), state=CreateMessageAF.choice)
async def process_change_send_time(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await state.update_data(data={
        'day': None,
        'hour': None,
        'minute': None
    })
    data = await state.get_data()
    keyboard = await get_day_send_msg_kb(data)
    text = 'Выберете день'
    await call.message.answer(text, reply_markup=keyboard)

    await CreateMessageAF.get_day_send.set()
