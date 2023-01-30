from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline.create_test import get_photo_result, get_result_photo_dt
from keyboard.inline.create_test.create_results import create_message_result, create_result_msg_keyboard
from loader import dp
from .get_main_message import send_main_message
from states import AddTest


@dp.callback_query_handler(create_message_result.filter(prefix='photo'), state=AddTest.create_result)
async def process_get(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    keyboard = await get_photo_result(data)
    text = 'Отправьте фото'
    if data['photo']:
        text = 'Выберете'
    else:
        await AddTest.get_photo.set()
    await call.message.delete()
    await call.message.answer(text, reply_markup=keyboard)


@dp.callback_query_handler(get_result_photo_dt.filter(prefix='change'), state=AddTest.create_result)
async def process_change(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await AddTest.get_photo.set()
    await state.update_data(data={
        'photo': None
    })
    data = await state.get_data()
    keyboard = await get_photo_result(data)
    await call.message.edit_text('Отправьте фото', reply_markup=keyboard)
    await AddTest.get_photo.set()


@dp.message_handler(state=AddTest.get_photo, content_types=types.ContentTypes.PHOTO)
async def process_add(message: types.Message, state: FSMContext):
    photo = message.photo[-1].file_id
    await state.update_data(data={
        'photo': photo
    })
    await AddTest.create_result.set()
    data = await state.get_data()
    await send_main_message(data=data, message=message)


