from aiogram import types

from filters import IsAdmin
from keyboard.inline.users.get_product import get_products_mu, mu_product_data
from keyboard.inline.users.get_product_category import get_product_store_mu, mu_category_data
from keyboard.inline.users.manage_users import manage_users_dt, get_manage_users_kb
from loader import dp, bot
from modules.DataBase import get_user_by_id, create_shoplist_record, get_product_by_id


@dp.callback_query_handler(manage_users_dt.filter(prefix='add_product'), IsAdmin())
async def process_add_product(call: types.CallbackQuery, callback_data: dict):
    user_id = int(callback_data.get('user_id'))
    await call.answer(cache_time=1)
    keyboard = await get_product_store_mu(user_id)
    await bot.send_message(chat_id=call.from_user.id, text='Выберете категорию', reply_markup=keyboard)


@dp.callback_query_handler(manage_users_dt.filter(prefix='add_product'))
async def process_add_ct_and_get_product(call: types.CallbackQuery):
    await call.answer(cache_time=1, text='Вы не имеете доступ к этому функционалу', show_alert=True)


@dp.callback_query_handler(mu_category_data.filter())
async def process_add_ct_and_get_product(call: types.CallbackQuery, callback_data: dict):
    user_id = int(callback_data.get('us_id'))
    category_id = int(callback_data.get('ct_id'))
    await call.answer(cache_time=1)
    keyboard = await get_products_mu(category_id, user_id)
    await call.message.edit_text('Выберете продукт', reply_markup=keyboard)


@dp.callback_query_handler(mu_product_data.filter())
async def process_add_product_user(call: types.CallbackQuery, callback_data: dict):
    user_id = int(callback_data.get('us_id'))
    product_id = int(callback_data.get('pr_id'))

    user = get_user_by_id(user_id)
    text = f'Пользователь: {user.name} \n' \
           f'Телефон: {user.phone_number} \n' \
           f'Зарегистрировался: {user.ts}\n' \
           f'Стадия: {user.stage}'

    product = get_product_by_id(product_id)
    if product.price:
        price = product.price
    else:
        price = 0
    create_shoplist_record(user.tg_id, product_id, price)
    keyboard = await get_manage_users_kb(user.id)
    await call.answer(text='Продукт успешно выдан', show_alert=True)
    await bot.send_message(chat_id=user.tg_id,
                           text=f'Вам был выдан продукт "{product.name}"')
    await call.message.edit_text(text, reply_markup=keyboard)
