from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline.create_test import get_photo_result, get_result_photo_dt, get_audio_result, get_result_audio_dt
from keyboard.inline.create_test.create_results import create_message_result, create_result_msg_keyboard
from loader import dp
from .get_main_message import send_main_message
from states import AddTest


@dp.callback_query_handler(create_message_result.filter(prefix='audio'), state=AddTest.create_result)
async def process_get(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    keyboard = await get_audio_result(data)
    text = 'Отправьте аудио'
    if data['audio']:
        text = 'Выберете'
    else:
        await AddTest.get_audio.set()
    await call.message.delete()
    await call.message.answer(text, reply_markup=keyboard)


@dp.callback_query_handler(get_result_audio_dt.filter(prefix='change'), state=AddTest.create_result)
async def process_change(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await AddTest.get_photo.set()
    await state.update_data(data={
        'audio': None
    })
    data = await state.get_data()
    keyboard = await get_audio_result(data)
    await call.message.edit_text('Отправьте аудио', reply_markup=keyboard)
    await AddTest.get_photo.set()


@dp.message_handler(state=AddTest.get_audio, content_types=types.ContentTypes.AUDIO)
async def process_add(message: types.Message, state: FSMContext):
    audio = message.audio.file_id
    await state.update_data(data={
        'audio': audio
    })
    await AddTest.create_result.set()
    data = await state.get_data()
    await send_main_message(data=data, message=message)


