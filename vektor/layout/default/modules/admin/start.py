from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp
from modules.BotKeyboards import admin_main
from modules.Credentials import ADMINS
from modules.DataBase import get_admins


@dp.message_handler(Command('admin'), user_id=ADMINS)
async def start_admin(message: types.Message):
    await message.answer('Управление', reply_markup=admin_main)

@dp.message_handler(Command('admin'))
async def start_admin(message: types.Message):
    user_id = [int(admin.tg_id) for admin in get_admins()]
    print(user_id)
    if message.from_user.id in user_id:
        await message.answer('Управление', reply_markup=admin_main)