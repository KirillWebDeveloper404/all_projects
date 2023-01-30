from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline import create_message_af, generate_get_video_note_keyboard, msg_video_note_af_data
from loader import dp
from states import CreateMessageAF
from .get_main_text import send_main_text


@dp.callback_query_handler(create_message_af.filter(prefix='video_note'), state=CreateMessageAF.choice)
async def process_add_video_note_message(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    data = await state.get_data()
    keyboard = await generate_get_video_note_keyboard(data)
    await call.message.delete()
    if data['video_note']:
        await call.message.answer('Выберете:', reply_markup=keyboard)
    else:
        await call.message.answer('Отправьте видео кружочек:', reply_markup=keyboard)
        await CreateMessageAF.get_video_note.set()


@dp.message_handler(state=CreateMessageAF.get_video_note, content_types=types.ContentTypes.VIDEO_NOTE)
async def process_get_video_note_message(message: types.Message, state: FSMContext):
    video_note = message.video_note.file_id
    await state.update_data(data={
        'video_note': video_note
    })
    data = await state.get_data()
    await send_main_text(data, message)
    await CreateMessageAF.choice.set()


@dp.message_handler(state=CreateMessageAF.get_video_note, content_types=types.ContentTypes.ANY)
async def process_get_audio_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    keyboard = await generate_get_video_note_keyboard(data)
    await message.answer('Вы отправили не тот файл, отправьте мне нужный файл.', reply_markup=keyboard)


@dp.callback_query_handler(msg_video_note_af_data.filter(prefix='change_video_note'), state=CreateMessageAF.choice)
async def process_change_video_note_message(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await state.update_data(data={
        'video_note': None
    })
    data = await state.get_data()
    keyboard = await generate_get_video_note_keyboard(data)
    await call.message.edit_text('Отправьте видео кружочек:', reply_markup=keyboard)
    await CreateMessageAF.get_video_note.set()
