from aiogram import types

from keyboard.inline.tests.main import test_main_data, test_main
from loader import dp
from modules.BotKeyboards import admin_dt, admin_main


@dp.callback_query_handler(admin_dt.filter(prefix='tests'))
async def process_start_tests(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text('Квизы', reply_markup=test_main)


@dp.callback_query_handler(test_main_data.filter(prefix='back'))
async def process_back_to_main_menu(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text('Управление', reply_markup=admin_main)
