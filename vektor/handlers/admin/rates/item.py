from aiogram import types

from handlers.admin.rates.get_info import send_item_rate
from keyboards.inline.admin.item_rate import item_rate_data
from keyboards.inline.admin.list_rates import list_rates_data, get_list_rates_kb
from keyboards.inline.admin.rates_main import rates_main
from loader import dp
from utils.db_api.rates_model import del_rate_by_id


@dp.callback_query_handler(list_rates_data.filter(pr='item'))
async def process_item(call: types.CallbackQuery, callback_data: dict):
    rate_id = int(callback_data.get('rate_id'))
    await send_item_rate(rate_id, call.message, is_delete=True)


@dp.callback_query_handler(item_rate_data.filter(pr='back'))
async def process_back(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    keyboard = await get_list_rates_kb()
    if not keyboard:
        await call.message.edit_text('Тарифы', reply_markup=rates_main)
        return
    await call.message.delete()
    await call.message.answer('Список тарифов', reply_markup=keyboard)


@dp.callback_query_handler(item_rate_data.filter(pr='delete'))
async def process_delete(call: types.CallbackQuery, callback_data: dict):
    rate_id = int(callback_data.get("rate_id"))
    # await call.answer(cache_time=1, text='В разработке', show_alert=True)

    # Delete a rate from in the database
    await del_rate_by_id(rate_id)

    # back
    await process_back(call)






