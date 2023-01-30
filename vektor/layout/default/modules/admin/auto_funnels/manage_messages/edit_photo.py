from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline.edit.edit_message import edit_message_kb_data, generate_edit_messages_keyboard
from keyboard.inline.edit.edit_photo import generate_get_photo_keyboard, edit_photo_msg_data
from loader import dp
from states import EditMessages
from utils.functions.edit_messages_msg import get_text_edit_messages


@dp.callback_query_handler(edit_message_kb_data.filter(prefix='photo'), state=EditMessages.start)
async def process_start_edit(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await call.message.delete()
    data = await state.get_data()
    keyboard = await generate_get_photo_keyboard(data)
    if data['photo']:
        text = 'Выберете:'
    else:
        text = 'Отправьте фото'
        await EditMessages.photo.set()
    await call.message.answer(text, reply_markup=keyboard)


@dp.message_handler(state=EditMessages.photo, content_types=types.ContentTypes.PHOTO)
async def process_get(message: types.Message, state: FSMContext):
    photo = message.photo[-1].file_id
    await state.update_data(data={
        'photo': photo
    })
    data = await state.get_data()
    await get_text_edit_messages(data, message)
    await EditMessages.start.set()


@dp.callback_query_handler(edit_photo_msg_data.filter(prefix='change'), state=EditMessages.start)
async def process_change(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await state.update_data(data={
        'photo': None
    })
    text = 'Отправьте фото'
    data = await state.get_data()
    keyboard = await generate_get_photo_keyboard(data)
    await EditMessages.photo.set()
    await call.message.answer(text, reply_markup=keyboard)


@dp.message_handler(state=EditMessages.photo, content_types=types.ContentTypes.ANY)
async def process_error_file(message: types.Message):
    await message.answer('Вы отправили не тот тип файла')
