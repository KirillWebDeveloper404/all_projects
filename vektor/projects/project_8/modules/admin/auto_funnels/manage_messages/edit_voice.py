from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline.edit.edit_message import edit_message_kb_data
from keyboard.inline.edit.edit_voice import generate_get_voice_keyboard, edit_voice_msg_data
from loader import dp
from states import EditMessages
from utils.functions.edit_messages_msg import get_text_edit_messages


@dp.callback_query_handler(edit_message_kb_data.filter(prefix='voice'), state=EditMessages.start)
async def process_start_edit(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await call.message.delete()
    data = await state.get_data()
    keyboard = await generate_get_voice_keyboard(data)
    if data['voice']:
        text = 'Выберете:'
    else:
        text = 'Отправьте аудио'
        await EditMessages.voice.set()
    await call.message.answer(text, reply_markup=keyboard)


@dp.message_handler(state=EditMessages.voice, content_types=types.ContentTypes.VOICE)
async def process_get(message: types.Message, state: FSMContext):
    voice = message.voice.file_id
    await state.update_data(data={
        'voice': voice
    })
    data = await state.get_data()
    await get_text_edit_messages(data, message)
    await EditMessages.start.set()


@dp.callback_query_handler(edit_voice_msg_data.filter(prefix='change'), state=EditMessages.start)
async def process_change(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await state.update_data(data={
        'voice': None
    })
    text = 'Отправьте аудио'
    data = await state.get_data()
    keyboard = await generate_get_voice_keyboard(data)
    await EditMessages.voice.set()
    await call.message.answer(text, reply_markup=keyboard)


@dp.message_handler(state=EditMessages.voice, content_types=types.ContentTypes.ANY)
async def process_error_file(message: types.Message):
    await message.answer('Вы отправили не тот тип файла')
