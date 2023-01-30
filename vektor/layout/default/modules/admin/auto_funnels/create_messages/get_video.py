from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline import create_message_af, msg_video_af_data, \
    generate_get_video_keyboard
from loader import dp
from states import CreateMessageAF
from .get_main_text import send_main_text


@dp.callback_query_handler(create_message_af.filter(prefix='video'), state=CreateMessageAF.choice)
async def process_add_video_message(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    data = await state.get_data()
    keyboard = await generate_get_video_keyboard(data)
    await call.message.delete()
    if data['video']:
        await call.message.answer('Выберете:', reply_markup=keyboard)
    else:
        await call.message.answer('Отправьте видео:', reply_markup=keyboard)
        await CreateMessageAF.get_video.set()


@dp.message_handler(state=CreateMessageAF.get_video, content_types=types.ContentTypes.VIDEO)
async def process_get_video_message(message: types.Message, state: FSMContext):
    video = message.video.file_id
    await state.update_data(data={
        'video': video
    })
    data = await state.get_data()
    await send_main_text(data, message)
    await CreateMessageAF.choice.set()


@dp.message_handler(state=CreateMessageAF.get_video, content_types=types.ContentTypes.ANY)
async def process_get_audio_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    keyboard = await generate_get_video_keyboard(data)
    await message.answer('Вы отправили не тот файл, отправьте мне нужный файл.', reply_markup=keyboard)


@dp.callback_query_handler(msg_video_af_data.filter(prefix='change_video'), state=CreateMessageAF.choice)
async def process_change_video_message(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await state.update_data(data={
        'video': None
    })
    data = await state.get_data()
    keyboard = await generate_get_video_keyboard(data)
    await call.message.edit_text('Отправьте видео:', reply_markup=keyboard)
    await CreateMessageAF.get_video.set()
