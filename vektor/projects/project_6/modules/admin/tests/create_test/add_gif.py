from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline.create_test import get_photo_result
from keyboard.inline.create_test.create_results import create_message_result
from keyboard.inline.create_test.get_result_gif import get_result_gif_dt, get_gif_result
from loader import dp
from states import AddTest
from .get_main_message import send_main_message


@dp.callback_query_handler(create_message_result.filter(prefix='gif'), state=AddTest.create_result)
async def process_get(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    keyboard = await get_gif_result(data)
    text = 'Отправьте гифку'
    if data['gif']:
        text = 'Выберете'
    else:
        await AddTest.get_gif.set()
    await call.message.delete()
    await call.message.answer(text, reply_markup=keyboard)


@dp.callback_query_handler(get_result_gif_dt.filter(prefix='change'), state=AddTest.create_result)
async def process_change(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await state.update_data(data={
        'gif': None
    })
    data = await state.get_data()
    keyboard = await get_gif_result(data)
    await call.message.edit_text('Отправьте гифку', reply_markup=keyboard)
    await AddTest.get_gif.set()


@dp.message_handler(state=AddTest.get_gif, content_types=types.ContentTypes.ANIMATION)
async def process_add(message: types.Message, state: FSMContext):
    gif = message.animation.file_id
    await state.update_data(data={
        'gif': gif
    })
    data = await state.get_data()
    await AddTest.create_result.set()
    await send_main_message(data=data, message=message)


