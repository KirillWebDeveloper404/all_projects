from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline import create_message_af, msg_voice_af_data, \
    generate_get_voice_keyboard
from loader import dp
from states import CreateMessageAF
from .get_main_text import send_main_text


@dp.callback_query_handler(create_message_af.filter(prefix='voice'), state=CreateMessageAF.choice)
async def process_add_voice_message(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    data = await state.get_data()
    keyboard = await generate_get_voice_keyboard(data)
    await call.message.delete()
    if data['voice']:
        await call.message.answer('Выберете:', reply_markup=keyboard)
    else:
        await call.message.answer('Отправьте голосовое сообщение:', reply_markup=keyboard)
        await CreateMessageAF.get_voice.set()


@dp.message_handler(state=CreateMessageAF.get_voice, content_types=types.ContentTypes.VOICE)
async def process_get_voice_message(message: types.Message, state: FSMContext):
    voice = message.voice.file_id
    await state.update_data(data={
        'voice': voice
    })
    data = await state.get_data()
    await send_main_text(data, message)
    await CreateMessageAF.choice.set()


@dp.message_handler(state=CreateMessageAF.get_voice, content_types=types.ContentTypes.ANY)
async def process_get_audio_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    keyboard = await generate_get_voice_keyboard(data)
    await message.answer('Вы отправили не тот файл, отправьте мне нужный файл.', reply_markup=keyboard)


@dp.callback_query_handler(msg_voice_af_data.filter(prefix='change_voice'), state=CreateMessageAF.choice)
async def process_change_voice_message(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await state.update_data(data={
        'voice': None
    })
    data = await state.get_data()
    keyboard = await generate_get_voice_keyboard(data)
    await call.message.edit_text('Отправьте голосовое сообщение:', reply_markup=keyboard)
    await CreateMessageAF.get_voice.set()
