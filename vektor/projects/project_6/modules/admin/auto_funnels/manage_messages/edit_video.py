from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline.edit.edit_gif import generate_get_gif_keyboard, edit_gif_msg_data
from keyboard.inline.edit.edit_message import edit_message_kb_data
from keyboard.inline.edit.edit_video import generate_get_video_keyboard, edit_video_msg_data
from loader import dp
from states import EditMessages
from utils.functions.edit_messages_msg import get_text_edit_messages


@dp.callback_query_handler(edit_message_kb_data.filter(prefix='video'), state=EditMessages.start)
async def process_start_edit(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    data = await state.get_data()
    await call.message.delete()
    keyboard = await generate_get_video_keyboard(data)
    if data['video']:
        text = 'Выберете:'
    else:
        text = 'Отправьте видео'
        await EditMessages.video.set()
    await call.message.answer(text, reply_markup=keyboard)


@dp.message_handler(state=EditMessages.video, content_types=types.ContentTypes.VIDEO)
async def process_get(message: types.Message, state: FSMContext):
    video = message.video.file_id
    await state.update_data(data={
        'video': video
    })
    data = await state.get_data()
    await get_text_edit_messages(data, message)
    await EditMessages.start.set()


@dp.callback_query_handler(edit_video_msg_data.filter(prefix='change'), state=EditMessages.start)
async def process_change(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await state.update_data(data={
        'video': None
    })
    text = 'Отправьте видео'
    data = await state.get_data()
    keyboard = await generate_get_video_keyboard(data)
    await EditMessages.video.set()
    await call.message.answer(text, reply_markup=keyboard)


@dp.message_handler(state=EditMessages.video, content_types=types.ContentTypes.ANY)
async def process_error_file(message: types.Message):
    await message.answer('Вы отправили не тот тип файла')
