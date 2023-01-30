from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline.create_test import get_photo_result, get_result_photo_dt, get_audio_result, get_result_voice_dt, \
    get_voice_result, get_result_video_note_dt, get_video_note_result
from keyboard.inline.create_test.create_results import create_message_result, create_result_msg_keyboard
from loader import dp
from .get_main_message import send_main_message
from states import AddTest


@dp.callback_query_handler(create_message_result.filter(prefix='video_note'), state=AddTest.create_result)
async def process_get(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    keyboard = await get_video_note_result(data)
    text = 'Отправьте видео кружочек'
    if data['video_note']:
        text = 'Выберете'
    else:
        await AddTest.get_video_note.set()
    await call.message.delete()
    await call.message.answer(text, reply_markup=keyboard)


@dp.callback_query_handler(get_result_video_note_dt.filter(prefix='change'), state=AddTest.create_result)
async def process_change(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await state.update_data(data={
        'video_note': None
    })
    data = await state.get_data()
    keyboard = await get_video_note_result(data)
    await call.message.edit_text('Отправьте видео кружочек', reply_markup=keyboard)
    await AddTest.get_video_note.set()


@dp.message_handler(state=AddTest.get_video_note, content_types=types.ContentTypes.VIDEO_NOTE)
async def process_add(message: types.Message, state: FSMContext):
    video_note = message.video_note.file_id
    await state.update_data(data={
        'video_note': video_note
    })
    await AddTest.create_result.set()
    data = await state.get_data()
    await send_main_message(data=data, message=message)


