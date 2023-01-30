from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline import create_message_af, msg_gif_af_data, generate_get_gif_keyboard
from loader import dp
from states import CreateMessageAF
from .get_main_text import send_main_text


@dp.callback_query_handler(create_message_af.filter(prefix='gif'), state=CreateMessageAF.choice)
async def process_add_gif_message(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    data = await state.get_data()
    keyboard = await generate_get_gif_keyboard(data)
    await call.message.delete()
    if data['gif']:
        await call.message.answer('Выберете:', reply_markup=keyboard)
    else:
        await call.message.answer('Отправьте анимацию(GIF):', reply_markup=keyboard)
        await CreateMessageAF.get_gif.set()


@dp.message_handler(state=CreateMessageAF.get_gif, content_types=types.ContentTypes.ANIMATION)
async def process_get_gif_message(message: types.Message, state: FSMContext):
    gif = message.animation.file_id
    await state.update_data(data={
        'gif': gif
    })
    data = await state.get_data()
    await send_main_text(data, message)
    await CreateMessageAF.choice.set()


@dp.message_handler(state=CreateMessageAF.get_gif, content_types=types.ContentTypes.ANY)
async def process_get_audio_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    keyboard = await generate_get_gif_keyboard(data)
    await message.answer('Вы отправили не тот файл, отправьте мне нужный файл.', reply_markup=keyboard)


@dp.callback_query_handler(msg_gif_af_data.filter(prefix='change_gif'), state=CreateMessageAF.choice)
async def process_change_gif_message(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await state.update_data(data={
        'gif': None
    })
    data = await state.get_data()
    keyboard = await generate_get_gif_keyboard(data)
    await call.message.edit_text('Отправьте анимацию:', reply_markup=keyboard)
    await CreateMessageAF.get_gif.set()
