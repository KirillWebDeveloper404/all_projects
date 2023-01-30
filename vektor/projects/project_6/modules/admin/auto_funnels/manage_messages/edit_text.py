from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline.edit.edit_message import edit_message_kb_data
from keyboard.inline.edit.edit_text import edit_text_msg_data, generate_get_text_keyboard
from loader import dp
from states import EditMessages
from utils.functions.edit_messages_msg import get_text_edit_messages


@dp.callback_query_handler(edit_message_kb_data.filter(prefix='text'), state=EditMessages.start)
async def process_start_edit(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await call.message.delete()
    data = await state.get_data()
    keyboard = await generate_get_text_keyboard(data)
    if data['text']:
        text = 'Выберете:'
    else:
        text = 'Отправьте сообщение'
        await EditMessages.text.set()
    await call.message.answer(text, reply_markup=keyboard)


@dp.message_handler(state=EditMessages.text)
async def process_get(message: types.Message, state: FSMContext):
    text = message.text
    await state.update_data(data={
        'text': text
    })
    data = await state.get_data()
    await get_text_edit_messages(data, message)
    await EditMessages.start.set()


@dp.callback_query_handler(edit_text_msg_data.filter(prefix='change'), state=EditMessages.start)
async def process_change(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await state.update_data(data={
        'text': None
    })
    text = 'Отправьте сообщение'
    data = await state.get_data()
    keyboard = await generate_get_text_keyboard(data)
    await EditMessages.text.set()
    await call.message.answer(text, reply_markup=keyboard)


@dp.message_handler(state=EditMessages.text, content_types=types.ContentTypes.ANY)
async def process_error_file(message: types.Message):
    await message.answer('Вы отправили не тот тип сообщение')
