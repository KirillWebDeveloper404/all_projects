"""Под большим вопросом"""

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline import create_message_af, generate_get_msg_send_time_keyboard, msg_send_time_data, \
    generate_get_msg_interval_keyboard, msg_interval_data, delete_time_data, delete_time_kb
from keyboard.inline.create_message_af.get_msgs_for_interval import get_keyboard_for_interval_msgs, \
    reference_interval_msgs_data
from loader import dp
from .get_main_text import send_main_text
from states import CreateMessageAF


@dp.callback_query_handler(create_message_af.filter(prefix='interval'), state=CreateMessageAF.choice)
async def process_adding_interval(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    data = await state.get_data()
    await call.message.delete()
    if (data['interval_hour'] or data['interval_minute'] or data['interval_second'] or data['interval_day']) \
            and data['interval_msg']:
        keyboard = await generate_get_msg_interval_keyboard(data=data)
        await call.message.answer('Выберете:', reply_markup=keyboard)
    else:
        keyboard = await get_keyboard_for_interval_msgs(data)
        text = 'Выберете сообщение от которого будет интервал:'
        await call.message.answer(text, reply_markup=keyboard)
        await CreateMessageAF.get_msg_interval.set()


@dp.callback_query_handler(reference_interval_msgs_data.filter(), state=CreateMessageAF.get_msg_interval)
async def get_interval(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    interval_msg = callback_data.get('msg_id')
    await state.update_data(data={
        'interval_msg': interval_msg,
    })
    await call.message.edit_text('Выберете через сколько сообщение отправится пользователю',
                                 reply_markup=delete_time_kb)
    await CreateMessageAF.get_interval_time.set()


@dp.callback_query_handler(delete_time_data.filter(), state=CreateMessageAF.get_interval_time)
async def get_interval_time(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    day = int(callback_data.get('day'))
    hour = int(callback_data.get('hour'))
    minute = int(callback_data.get('minute'))
    second = int(callback_data.get('second'))
    await state.update_data(data={
        'interval_hour': hour,
        'interval_minute': minute,
        'interval_second': second,
        'interval_day': day,
    })
    data = await state.get_data()
    await send_main_text(data, call.message, True)
    await CreateMessageAF.choice.set()


@dp.callback_query_handler(msg_interval_data.filter(prefix='change_interval'), state=CreateMessageAF.choice)
async def process_change_interval(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await state.update_data(data={
        'interval_msg': None,
        'interval_hour': None,
        'interval_minute': None,
        'interval_second': None,
        'interval_day': None,
    })
    data = await state.get_data()
    keyboard = await get_keyboard_for_interval_msgs(data=data)
    text = 'Выберете сообщение от которого будет интервал:'
    await call.message.answer(text, reply_markup=keyboard)

    await CreateMessageAF.get_msg_interval.set()
