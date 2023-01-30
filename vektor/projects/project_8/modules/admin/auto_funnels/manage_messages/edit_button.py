from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline import generate_get_msg_button_keyboard, msg_button_data, \
    generate_get_msg_button_change_keyboard
from keyboard.inline.edit.edit_button import generate_edit_button
from keyboard.inline.edit.edit_message import edit_message_kb_data
from loader import dp
from states import EditMessages
from utils.functions.edit_messages_msg import get_text_edit_messages


@dp.callback_query_handler(edit_message_kb_data.filter(prefix='button_link'), state=EditMessages.start)
async def process_start_edit(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    data = await state.get_data()
    await call.message.delete()
    keyboard = await generate_edit_button(data)
    if data['link']:
        await call.message.answer('Выберете:', reply_markup=keyboard)
    else:
        text = 'Введите ссылку:'
        await call.message.answer(text, reply_markup=keyboard)
        await EditMessages.link.set()


@dp.message_handler(state=EditMessages.link)
async def get_link(message: types.Message, state: FSMContext):
    link = message.text
    data = await state.get_data()
    if not ('http://' in link) and not ('https://' in link):
        keyboard = await generate_edit_button(data)
        await message.answer('Сообщение не содержит ссылки, отправьте ссылку', reply_markup=keyboard)
        return
    await state.update_data(data={
        'link': link,
        'text_link': 'Подробнее'
    })
    keyboard = await generate_edit_button(data)
    await message.answer('Введите текст кнопки, если вы не введете и нажмете « Назад, текст кнопки будет "Подробнее"',
                         reply_markup=keyboard)
    await EditMessages.text_link.set()


@dp.message_handler(state=EditMessages.link, content_types=types.ContentTypes.ANY)
async def process_get_audio_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    keyboard = await generate_edit_button(data)
    await message.answer('Вы отправили не текст, отправьте мне текст.', reply_markup=keyboard)


@dp.message_handler(state=EditMessages.text_link)
async def get_text_link(message: types.Message, state: FSMContext):
    text_link = message.text
    await state.update_data(data={
        'text_link': text_link
    })
    data = await state.get_data()
    await EditMessages.start.set()
    await get_text_edit_messages(data, message)


@dp.message_handler(state=EditMessages.text_link, content_types=types.ContentTypes.ANY)
async def process_get_audio_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    keyboard = await generate_edit_button(data)
    await message.answer('Вы отправили не текст, отправьте мне текст.', reply_markup=keyboard)


@dp.callback_query_handler(msg_button_data.filter(prefix='change'), state=EditMessages.start)
async def process_change_send_time(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await state.update_data(data={
        'text_link': None,
        'link': None,
    })
    data = await state.get_data()
    keyboard = await generate_edit_button(data)
    text = 'Введите ссылку:'
    await call.message.answer(text, reply_markup=keyboard)
    await EditMessages.link.set()
