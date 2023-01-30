from aiogram import types

from loader import dp
from modules.BotKeyboards import admin_dt, \
    employees_kb, employees_dt, admin_main


@dp.callback_query_handler(admin_dt.filter(prefix='employees'))
async def process_get_employees(call: types.CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=employees_kb)
    await call.answer()


@dp.callback_query_handler(employees_dt.filter(prefix='back'))
async def process_get_admin_main(call: types.CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=admin_main)
    await call.answer()
