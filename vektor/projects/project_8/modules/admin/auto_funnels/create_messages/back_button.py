from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline import msg_text_af_data, msg_photo_af_data, msg_gif_af_data, msg_video_af_data, msg_audio_af_data, \
    msg_voice_af_data, msg_video_note_af_data, msg_document_af_data, msg_send_time_data, msg_delete_hour_data, \
    msg_button_data, day_send_msg_data, time_send_msg_data, delete_time_data, msg_interval_data
from keyboard.inline.create_message_af.get_msg_test import msg_test_af_data
from loader import dp
from .get_main_text import send_main_text
from states import CreateMessageAF


@dp.callback_query_handler(msg_text_af_data.filter(prefix='back'),
                           state=[CreateMessageAF.get_text, CreateMessageAF.choice])
@dp.callback_query_handler(msg_video_af_data.filter(prefix='back'),
                           state=[CreateMessageAF.get_video, CreateMessageAF.choice])
@dp.callback_query_handler(msg_video_note_af_data.filter(prefix='back'),
                           state=[CreateMessageAF.get_video_note, CreateMessageAF.choice])
@dp.callback_query_handler(msg_gif_af_data.filter(prefix='back'),
                           state=[CreateMessageAF.get_gif, CreateMessageAF.choice])
@dp.callback_query_handler(msg_photo_af_data.filter(prefix='back'),
                           state=[CreateMessageAF.get_photo, CreateMessageAF.choice])
@dp.callback_query_handler(msg_audio_af_data.filter(prefix='back'),
                           state=[CreateMessageAF.get_audio, CreateMessageAF.choice])
@dp.callback_query_handler(msg_voice_af_data.filter(prefix='back'),
                           state=[CreateMessageAF.get_voice, CreateMessageAF.choice])
@dp.callback_query_handler(msg_document_af_data.filter(prefix='back'),
                           state=[CreateMessageAF.get_document, CreateMessageAF.choice])
@dp.callback_query_handler(msg_delete_hour_data.filter(prefix='back'),
                           state=[CreateMessageAF.get_delete_hour, CreateMessageAF.choice])
@dp.callback_query_handler(msg_button_data.filter(prefix='back'),
                           state=[CreateMessageAF.get_link, CreateMessageAF.choice, CreateMessageAF.get_text_link])
@dp.callback_query_handler(day_send_msg_data.filter(day='back'),
                           state=[CreateMessageAF.get_day_send, CreateMessageAF.get_time_send, CreateMessageAF.choice])
@dp.callback_query_handler(delete_time_data.filter(day='back'),
                           state=[CreateMessageAF.get_delete_hour, CreateMessageAF.choice,
                                  CreateMessageAF.get_interval_time])
@dp.callback_query_handler(time_send_msg_data.filter(hour='back'),
                           state=[CreateMessageAF.get_day_send, CreateMessageAF.get_time_send, CreateMessageAF.choice])
@dp.callback_query_handler(msg_send_time_data.filter(prefix='back'), state=[
    CreateMessageAF.get_day_send, CreateMessageAF.get_time_send, CreateMessageAF.choice
])
@dp.callback_query_handler(msg_interval_data.filter(prefix='back'), state=[
    CreateMessageAF.get_msg_interval, CreateMessageAF.get_interval_time, CreateMessageAF.choice
])
@dp.callback_query_handler(msg_test_af_data.filter(prefix='back'), state=CreateMessageAF.all_states)
async def process_change_text_message(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    data = await state.get_data()
    await send_main_text(data, call.message, True)
    await CreateMessageAF.choice.set()
