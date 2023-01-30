from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline import create_message_af
from loader import dp
from modules.admin.auto_funnels.create_messages.get_main_text import send_main_text
from states import CreateMessageAF


@dp.callback_query_handler(create_message_af.filter(prefix='clear'), state=CreateMessageAF.choice)
async def process_add_message_starting(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await state.update_data(data={
        'photo': None,
        'gif': None,
        'video': None,
        'audio': None,
        'voice': None,
        'video_note': None,
        'text': None,
        'test': None,
        'document': None,
        'day': None,
        'hour': None,
        'minute': None,
        'interval_msg': None,
        'interval_hour': None,
        'interval_minute': None,
        'delete_hour': None,
        'link': None,
        'text_link': None,
    })

    data = await state.get_data()
    await send_main_text(data, call.message, True)