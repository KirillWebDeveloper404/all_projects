from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline.edit.all_data import back_for_edit
from loader import dp
from states import EditMessages
from utils.functions.edit_messages_msg import get_text_edit_messages


@dp.callback_query_handler(back_for_edit.filter(), state=EditMessages.all_states)
async def process_back(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await call.message.delete()
    await EditMessages.start.set()
    data = await state.get_data()
    await state.update_data(data=data)
    await get_text_edit_messages(data, call.message)