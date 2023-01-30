from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import message

from keyboard.inline import create_message_af, generate_get_text_keyboard, msg_text_af_data
from loader import dp
from .get_main_text import send_main_text
from states import CreateMessageAF


@dp.callback_query_handler(create_message_af.filter(prefix='text'), state=CreateMessageAF.choice)
async def process_get_text_message(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    data = await state.get_data()
    keyboard = await generate_get_text_keyboard(data)
    await call.message.delete()
    if data['text']:
        await call.message.answer('Выберете:', reply_markup=keyboard)
    else:
        await call.message.answer('Введите текст:', reply_markup=keyboard)
        await CreateMessageAF.get_text.set()


@dp.message_handler(state=CreateMessageAF.get_text)
async def process_get_text_message(message: types.Message, state: FSMContext):
    text = message.text
    await state.update_data(data={
        'text': text
    })
    data = await state.get_data()
    await send_main_text(data, message)
    await CreateMessageAF.choice.set()


@dp.message_handler(state=CreateMessageAF.get_text, content_types=types.ContentTypes.ANY)
async def process_get_audio_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    keyboard = await generate_get_text_keyboard(data)
    await message.answer('Вы отправили не текст, отправьте мне текст.', reply_markup=keyboard)


@dp.callback_query_handler(msg_text_af_data.filter(prefix='change_text'), state=CreateMessageAF.choice)
async def process_change_text_message(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await state.update_data(data={
        'text': None
    })
    data = await state.get_data()
    keyboard = await generate_get_text_keyboard(data)
    await call.message.edit_text('Введите текст:', reply_markup=keyboard)
    await CreateMessageAF.get_text.set()
