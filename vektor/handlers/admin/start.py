from aiogram import types
from aiogram.dispatcher.filters import Command

from data.config import ADMINS
from keyboards.inline.admin.start import admin_start
from loader import dp


@dp.message_handler(Command('admin'), user_id=ADMINS)
async def process_start(message: types.Message):
    await message.answer('Админ-панель', reply_markup=admin_start)

