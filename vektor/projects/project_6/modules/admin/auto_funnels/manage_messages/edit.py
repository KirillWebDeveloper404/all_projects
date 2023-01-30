from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline.edit.edit_message import generate_edit_messages_keyboard
from keyboard.inline.manage_message.manage_message import manage_message_af_kb_data
from loader import dp
from modules.DataBase import get_message_af_by_id, MessageAutoFunnels
from states import EditMessages
from utils.functions.edit_messages_msg import get_text_edit_messages


@dp.callback_query_handler(manage_message_af_kb_data.filter(prefix='edit'))
async def process_start_edit_message(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await call.answer(cache_time=1)
    await call.message.delete()
    message_id = callback_data.get('message_id')
    message = get_message_af_by_id(message_id)

    data = {
        'message_id': message.id,
        'type_message': message.type_message,
        'photo': message.photo,
        'gif': message.gif,
        'document': message.document,
        'video': message.video,
        'video_note': message.video_note,
        'voice': message.voice,
        'audio': message.audio,
        'text': message.message_text,
        'text_link': message.text_link,
        'link': message.link,
        'delete_second': message.delete_second,
        'delete_minute': message.delete_minute,
        'delete_hour': message.delete_hour,
        'delete_day': message.delete_day,
        'send_day': message.day,
        'send_hour': message.hour,
        'send_minute': message.minute,
        'is_first': message.is_first,
        'interval_msg': message.interval_msg_id,
        'interval_second': message.interval_second,
        'interval_minute': message.interval_minute,
        'interval_hour': message.interval_hour,
        'interval_day': message.interval_day,
        'test': message.test,
    }

    await EditMessages.start.set()
    await state.update_data(data=data)
    await get_text_edit_messages(data, call.message)