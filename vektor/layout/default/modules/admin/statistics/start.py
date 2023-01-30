from aiogram import types

import modules.Config as Cfg
from keyboard.inline.statistics.start import statistics_main, statistics_main_data
from loader import dp
from modules.BotKeyboards import admin_dt, admin_main


@dp.callback_query_handler(admin_dt.filter(prefix="statistics"))
async def process_get_statistics(call: types.CallbackQuery):
    await call.answer(cache_time=1)

    await call.message.edit_text("Статистика", reply_markup=statistics_main)


@dp.callback_query_handler(statistics_main_data.filter(prefix='back'))
async def back_admin_panel(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text(Cfg.ADMIN_MSG, reply_markup=admin_main)



