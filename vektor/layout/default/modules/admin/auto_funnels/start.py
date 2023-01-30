from aiogram import types

from keyboard.inline import auto_funnels_menu, auto_funnels_menu_data
from loader import dp
from modules.BotKeyboards import admin_dt, admin_main


@dp.callback_query_handler(admin_dt.filter(prefix="auto_funnels"))
async def process_get_list_auto_funnels(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text('Автоворонки', reply_markup=auto_funnels_menu)


@dp.callback_query_handler(auto_funnels_menu_data.filter(prefix='back'))
async def process_back_to_admin_panel(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text('Управление', reply_markup=admin_main)