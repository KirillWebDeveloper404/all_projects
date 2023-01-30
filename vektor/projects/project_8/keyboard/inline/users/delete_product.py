from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from modules.DataBase import check_bought_products

is_buy_products_user_del = CallbackData('is_buy_products_user_del', 'us_id', 'pr_id')


async def get_products_user(user_id):
    inline_keyboard = []
    products = check_bought_products(user_id)
    for product in products:
        inline_keyboard.append([InlineKeyboardButton(product.product.name, callback_data=is_buy_products_user_del.new(
            us_id=user_id, pr_id=product.id
        ))])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
