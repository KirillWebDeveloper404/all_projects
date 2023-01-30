from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline.create_message_af.all_data import del_media
from loader import dp
from .get_main_text import send_main_text
from states import CreateMessageAF


@dp.callback_query_handler(del_media.filter(), state=CreateMessageAF.choice)
async def process_delete_media(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await state.update_data(data={
        'photo': None,
        'gif': None,
        'video': None,
        'audio': None,
        'voice': None,
        'video_note': None,
        'document': None,
    })
    data = await state.get_data()
    await send_main_text(data, call.message, True)
    await CreateMessageAF.choice.set()