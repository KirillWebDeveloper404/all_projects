from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

users_main_data = CallbackData('users_main_data', 'prefix')
users_main = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton('Выгрузка пользователей', callback_data=users_main_data.new(prefix='statistics'))
        ],
        [
            InlineKeyboardButton('« Назад', callback_data=users_main_data.new(prefix='back'))
        ]
    ]
)