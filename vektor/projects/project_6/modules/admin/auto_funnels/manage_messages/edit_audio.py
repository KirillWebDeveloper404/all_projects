from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline.edit.edit_audio import edit_audio_msg_data, generate_get_audio_keyboard
from keyboard.inline.edit.edit_message import edit_message_kb_data
from loader import dp
from states import EditMessages
from utils.functions.edit_messages_msg import get_text_edit_messages


@dp.callback_query_handler(edit_message_kb_data.filter(prefix='audio'), state=EditMessages.start)
async def process_start_edit(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    data = await state.get_data()
    await call.message.delete()
    keyboard = await generate_get_audio_keyboard(data)
    if data['audio']:
        text = 'Выберете:'
    else:
        text = 'Отправьте аудио'
        await EditMessages.audio.set()
    await call.message.answer(text, reply_markup=keyboard)


@dp.message_handler(state=EditMessages.audio, content_types=types.ContentTypes.AUDIO)
async def process_get(message: types.Message, state: FSMContext):
    audio = message.audio.file_id
    await state.update_data(data={
        'audio': audio
    })
    data = await state.get_data()
    await get_text_edit_messages(data, message)
    await EditMessages.start.set()


@dp.callback_query_handler(edit_audio_msg_data.filter(prefix='change'), state=EditMessages.start)
async def process_change(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await state.update_data(data={
        'audio': None
    })
    text = 'Отправьте аудио'
    data = await state.get_data()
    keyboard = await generate_get_audio_keyboard(data)
    await EditMessages.audio.set()
    await call.message.answer(text, reply_markup=keyboard)


@dp.message_handler(state=EditMessages.audio, content_types=types.ContentTypes.ANY)
async def process_error_file(message: types.Message):
    await message.answer('Вы отправили не тот тип файла')
