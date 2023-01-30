

"""
Регистрация по номеру телефона
"""
from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp
from modules.DataBase import get_user_by_tg_id, update_phone_number


@dp.message_handler(Command("register"))
async def register_by_phone(m: types.Message):
    markup = types.ReplyKeyboardMarkup([[types.KeyboardButton("Поделится номером", request_contact=True)]], resize_keyboard=True)
    user = get_user_by_tg_id(m.from_user.id)
    if not user.phone_number:
        await m.answer("Регистрация по номеру телефона. ", reply_markup=markup)
    else:
        await m.answer("Вы уже зарегистрированы")


@dp.message_handler(content_types=types.ContentType.CONTACT)
async def get_phone_user(m: types.Message, state="*"):
    phone_number = m.contact.phone_number
    user_id = m.contact.user_id

    update_phone_number(user_id, phone_number)
    await m.answer("Вы успешно зарегистрировались", reply_markup=types.ReplyKeyboardRemove())



