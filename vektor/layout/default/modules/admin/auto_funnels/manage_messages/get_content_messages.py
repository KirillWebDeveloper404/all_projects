from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline import auto_funnels_manage_messages_data, manage_messages
from keyboard.inline.manage_message.all_content_messages import get_all_content_messages_kb, content_message
from keyboard.inline.manage_message.manage_message import get_manage_messages_keyboard, manage_message_af_kb_data
from loader import dp
from modules.DataBase import get_first_message_by_funnel_id, get_message_af_by_id, get_all_content_messages_by_funnel_id
from utils.functions.send_manage_message_funnel import send_manage_message_funnel


@dp.callback_query_handler(auto_funnels_manage_messages_data.filter(prefix='content'))
async def process_get_content_messages(call: types.CallbackQuery, callback_data: dict):
    await call.message.delete()
    funnel_id = int(callback_data.get('id'))
    await call.answer(cache_time=1)
    keyboard = await get_all_content_messages_kb(funnel_id)
    await call.message.answer('Выберете сообщение', reply_markup=keyboard)


@dp.callback_query_handler(content_message.filter(message_id='None'))
async def process_back(call: types.CallbackQuery, callback_data: dict):
    await call.answer(cache_time=1)
    funnel_id = callback_data.get('funnel_id')
    keyboard = await manage_messages(funnel_id)

    await call.message.delete()
    await call.message.answer('Управление сообщениями в воронке', reply_markup=keyboard)


@dp.callback_query_handler(content_message.filter())
async def process_back(call: types.CallbackQuery, callback_data: dict):
    await call.message.delete()
    message_id = callback_data.get('message_id')
    await call.answer(cache_time=1)
    keyboard = await get_manage_messages_keyboard(message_id, 'content')
    await send_manage_message_funnel(message_id, call.from_user.id, keyboard=keyboard)


@dp.callback_query_handler(manage_message_af_kb_data.filter(prefix='content_back'))
async def process_back(call: types.CallbackQuery, callback_data:dict):
    message_id = int(callback_data.get('message_id'))
    message = get_message_af_by_id(message_id)
    await call.answer(cache_time=1)
    keyboard = await manage_messages(message.auto_funnel_id)
    await call.message.delete()
    await call.message.answer('Управление сообщениями в воронке', reply_markup=keyboard)
