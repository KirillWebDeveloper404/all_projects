from aiogram import types

from filters import IsAdmin
from keyboard.inline.users.delete_product import get_products_user, is_buy_products_user_del
from keyboard.inline.users.manage_users import manage_users_dt, get_manage_users_kb
from loader import bot, dp
from modules.DataBase import delete_product_user, get_user_by_id


@dp.callback_query_handler(manage_users_dt.filter(prefix='del_product'), IsAdmin())
async def process_add_product(call: types.CallbackQuery, callback_data: dict):
    user_id = int(callback_data.get('user_id'))
    await call.answer(cache_time=1)
    keyboard = await get_products_user(user_id)
    await bot.send_message(chat_id=call.from_user.id, text='Выберете товар для удаления', reply_markup=keyboard)


@dp.callback_query_handler(is_buy_products_user_del.filter())
async def process_delete_user_product(call: types.CallbackQuery, callback_data: dict):
    shop_id = int(callback_data.get('pr_id'))
    user_id = int(callback_data.get('us_id'))

    user = get_user_by_id(user_id)
    text = f'Пользователь: {user.name} \n' \
           f'Телефон: {user.phone_number} \n' \
           f'Зарегистрировался: {user.ts}\n' \
           f'Стадия: {user.stage}'

    delete_product_user(shop_id)
    keyboard = await get_manage_users_kb(user.id)
    await call.answer(text='Товар успешно удален', show_alert=True)
    await call.message.edit_text(text, reply_markup=keyboard)
