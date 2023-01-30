from aiogram import types

from keyboard.inline import generate_list_auto_funnels, auto_funnels_menu_data, \
    auto_funnels_menu, auto_funnels_list_data
from loader import dp


@dp.callback_query_handler(auto_funnels_menu_data.filter(prefix="list"))
async def process_get_list_auto_funnels(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    keyboard = await generate_list_auto_funnels()
    await call.message.edit_text('Список автоворонок', reply_markup=keyboard)


@dp.callback_query_handler(auto_funnels_list_data.filter(prefix='back'))
async def process_back_to_admin_panel(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text('Автоворонки', reply_markup=auto_funnels_menu)
