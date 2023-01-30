from aiogram import types

from loader import dp
from modules.BotKeyboards import admin_main, curator_changes_data, employees_kb


@dp.callback_query_handler(curator_changes_data.filter(prefix="back"))
async def process_back_curators(call: types.CallbackQuery):
    await call.answer()
    await call.message.edit_text("Управление", reply_markup=employees_kb)
