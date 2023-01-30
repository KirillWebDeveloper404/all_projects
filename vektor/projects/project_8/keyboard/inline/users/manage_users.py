from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

manage_users_dt = CallbackData('manage_users_dt', 'prefix', 'user_id')


async def get_manage_users_kb(user_id):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton('Выдать продукт', callback_data=manage_users_dt.new(
                    prefix='add_product', user_id=user_id
                ))
            ],
            [
                InlineKeyboardButton('Удалить продукт', callback_data=manage_users_dt.new(
                    prefix='del_product', user_id=user_id
                ))
            ],
        ]
    )
    return markup
