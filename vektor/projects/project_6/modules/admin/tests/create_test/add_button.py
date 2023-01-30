from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline.create_test.create_results import create_message_result
from keyboard.inline.create_test.get_result_button import get_button_result, get_result_button_dt
from loader import dp
from modules.admin.tests.create_test.get_main_message import send_main_message
from states import CreateMessageAF, AddTest


@dp.callback_query_handler(create_message_result.filter(prefix='button'), state=AddTest.create_result)
async def process_adding_button(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    data = await state.get_data()
    await call.message.delete()
    keyboard = await get_button_result(data)
    text = 'Добавьте ссылку'
    if data['link']:
        text = 'Выберете'
    else:
        await AddTest.get_link.set()

    await call.message.answer(text, reply_markup=keyboard)


@dp.message_handler(state=AddTest.get_link)
async def process_add_link(message: types.Message, state: FSMContext):
    link = message.text
    data = await state.get_data()
    keyboard = await get_button_result(data)
    if not ('http://' in link) and not ('https://' in link):
        await message.answer('Сообщение не содержит ссылки, отправьте ссылку', reply_markup=keyboard)
        return
    await state.update_data(data={
        'link': link,
        'text_link': 'Подробнее'
    })
    await AddTest.get_text_link.set()
    await message.answer('Добавьте текст кнопки', reply_markup=keyboard)


@dp.message_handler(state=AddTest.get_text_link)
async def process_add_link(message: types.Message, state: FSMContext):
    text_link = message.text
    await state.update_data(data={
        'text_link': text_link
    })
    data = await state.get_data()
    await AddTest.create_result.set()
    await send_main_message(data=data, message=message)


@dp.callback_query_handler(get_result_button_dt.filter(prefix='change'), state=AddTest.create_result)
async def process_change_link(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await state.update_data(data={
        'link': None,
        'text_link': None
    })
    data = await state.get_data()
    keyboard = await get_button_result(data)
    await call.message.edit_text('Добавьте ссылку', reply_markup=keyboard)
    await AddTest.get_link.set()
