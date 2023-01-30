from aiogram import types

from keyboard.inline.create_test import create_result_msg_keyboard


async def send_main_message(data, message: types.Message, delete=False):
    text = 'Тест'
    if delete:
        await message.delete()

    keyboard = await create_result_msg_keyboard(data)
    await message.answer(text=text, reply_markup=keyboard)
