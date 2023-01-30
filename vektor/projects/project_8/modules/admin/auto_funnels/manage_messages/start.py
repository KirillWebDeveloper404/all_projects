from aiogram import types

from keyboard.inline import auto_funnels_manage_data, manage_messages
from loader import dp


@dp.callback_query_handler(auto_funnels_manage_data.filter(prefix='messages'))
async def process_manage_messages_auto_funnels(call: types.CallbackQuery, callback_data: dict):
    funnel_id = int(callback_data.get('id'))
    await call.answer(cache_time=1)
    keyboard = await manage_messages(funnel_id)
    await call.message.edit_text('Управление сообщениями в воронке', reply_markup=keyboard)