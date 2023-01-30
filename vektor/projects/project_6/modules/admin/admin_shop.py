from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from modules.BotKeyboards import media_dt, admin_shop_data, admin_main, admin_shop_category, admin_shop_category_data, \
    admin_shop, admin_shop_product, admin_shop_product_data


@dp.callback_query_handler(admin_shop_data.filter(prefix='back'))
async def process_back_to_admin_panel(call: types.CallbackQuery):
    await call.message.edit_text('Управление', reply_markup=admin_main)
    await call.answer()


@dp.callback_query_handler(admin_shop_data.filter(prefix='category'))
async def process_get_category_manage(call: types.CallbackQuery):
    await call.answer()
    await call.message.edit_text('Категории', reply_markup=admin_shop_category)


@dp.callback_query_handler(admin_shop_data.filter(prefix='products'))
async def process_get_product_manage(call: types.CallbackQuery):
    await call.answer()
    await call.message.edit_text('Товары', reply_markup=admin_shop_product)


@dp.callback_query_handler(admin_shop_category_data.filter(prefix='back'))
async def process_back_product_manage(call: types.CallbackQuery):
    await call.answer()
    await call.message.edit_text('Управление', reply_markup=admin_shop)


@dp.callback_query_handler(admin_shop_product_data.filter(prefix='back'))
async def process_back_product_manage(call: types.CallbackQuery):
    await call.answer()
    await call.message.edit_text('Управление', reply_markup=admin_shop)