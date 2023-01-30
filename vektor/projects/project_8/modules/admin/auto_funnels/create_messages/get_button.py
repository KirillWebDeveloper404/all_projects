from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline import create_message_af, generate_get_msg_button_keyboard, msg_button_data, \
    generate_get_msg_button_change_keyboard
from loader import dp
from states import CreateMessageAF
from .get_main_text import send_main_text


@dp.callback_query_handler(create_message_af.filter(prefix='button_link'), state=CreateMessageAF.choice)
async def process_adding_button(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    data = await state.get_data()
    await call.message.delete()
    if data['link']:
        keyboard = await generate_get_msg_button_change_keyboard()
        await call.message.answer('Выберете:', reply_markup=keyboard)
    else:
        text = 'Введите ссылку:'
        keyboard = await generate_get_msg_button_keyboard()
        await call.message.answer(text, reply_markup=keyboard)
        await CreateMessageAF.get_link.set()


@dp.message_handler(state=CreateMessageAF.get_link)
async def get_link(message: types.Message, state: FSMContext):
    link = message.text
    if not ('http://' in link) and not ('https://' in link):
        keyboard = await generate_get_msg_button_keyboard()
        await message.answer('Сообщение не содержит ссылки, отправьте ссылку', reply_markup=keyboard)
        return
    await state.update_data(data={
        'link': link,
        'text_link': 'Подробнее'
    })
    keyboard = await generate_get_msg_button_keyboard()
    await message.answer('Введите текст кнопки, если вы не введете и нажмете « Назад, текст кнопки будет "Подробнее"',
                         reply_markup=keyboard)
    await CreateMessageAF.get_text_link.set()


@dp.message_handler(state=CreateMessageAF.get_link, content_types=types.ContentTypes.ANY)
async def process_get_audio_message(message: types.Message, state: FSMContext):
    keyboard = await generate_get_msg_button_keyboard()
    await message.answer('Вы отправили не текст, отправьте мне текст.', reply_markup=keyboard)


@dp.message_handler(state=CreateMessageAF.get_text_link)
async def get_text_link(message: types.Message, state: FSMContext):
    text_link = message.text
    await state.update_data(data={
        'text_link': text_link
    })
    data = await state.get_data()
    await send_main_text(data, message)
    await CreateMessageAF.choice.set()


@dp.message_handler(state=CreateMessageAF.get_text_link, content_types=types.ContentTypes.ANY)
async def process_get_audio_message(message: types.Message, state: FSMContext):
    keyboard = await generate_get_msg_button_keyboard()
    await message.answer('Вы отправили не текст, отправьте мне текст.', reply_markup=keyboard)


@dp.callback_query_handler(msg_button_data.filter(prefix='change_button_link'), state=CreateMessageAF.choice)
async def process_change_send_time(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await state.update_data(data={
        'text_link': None,
        'link': None,
    })
    keyboard = await generate_get_msg_button_keyboard()
    text = 'Введите ссылку:'
    await call.message.answer(text, reply_markup=keyboard)

    await CreateMessageAF.get_link.set()
