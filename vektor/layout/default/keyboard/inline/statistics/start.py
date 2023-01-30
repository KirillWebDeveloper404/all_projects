from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

statistics_main_data = CallbackData('statistics_main_data', 'prefix')

statistics_main = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Автоворонки', callback_data=statistics_main_data.new(prefix='funnel')),
        ],
        [
            InlineKeyboardButton(text='« Назад', callback_data=statistics_main_data.new(prefix='back')),
        ]
    ]
)