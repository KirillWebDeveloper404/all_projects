from aiogram import types

from keyboards.inline.admin.list_rates import get_list_rates_kb, list_rates_data
from keyboards.inline.admin.rates_main import rates_main_data, rates_main
from loader import dp


@dp.callback_query_handler(rates_main_data.filter(pr='list'))
async def process_list(call: types.CallbackQuery):
    keyboard = await get_list_rates_kb()
    if not keyboard:
        await call.answer(text='У вас пока что нет тарифов', show_alert=True, cache_time=1)
        return
    await call.answer(cache_time=1)
    await call.message.delete()
    await call.message.answer('Список тарифов', reply_markup=keyboard)


@dp.callback_query_handler(list_rates_data.filter(pr='back'))
async def process_back(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text('Тарифы', reply_markup=rates_main)
