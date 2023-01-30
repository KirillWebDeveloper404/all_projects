from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from modules.DataBase import get_products_by_category

mu_product_data = CallbackData('mu_prd_data', 'us_id', 'pr_id')


async def get_products_mu(category, user_id):
    client_store = InlineKeyboardMarkup()
    for product in get_products_by_category(category):
        client_store.row(
            InlineKeyboardButton(product.name, callback_data=mu_product_data.new(pr_id=product.id, us_id=user_id)))
    return client_store
