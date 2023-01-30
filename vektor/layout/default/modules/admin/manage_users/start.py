from aiogram import types

from keyboard.inline.users.main import users_main, users_main_data
from loader import dp
from modules.BotKeyboards import admin_dt, admin_main


@dp.callback_query_handler(admin_dt.filter(prefix='users'))
async def process_get_manage_users(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text('Управление пользователями', reply_markup=users_main)


@dp.callback_query_handler(users_main_data.filter(prefix='back'))
async def process_back_to_main_menu(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text('Управление', reply_markup=admin_main)