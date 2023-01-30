from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

delete_time_data = CallbackData('delete_time_data', 'day', 'hour', 'minute', 'second')

delete_time_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton('5 секунд', callback_data=delete_time_data.new(
                day=0, hour=0, minute=0, second=5
            )),
            InlineKeyboardButton('10 секунд', callback_data=delete_time_data.new(
                day=0, hour=0, minute=0, second=10
            )),
            InlineKeyboardButton('30 секунд', callback_data=delete_time_data.new(
                day=0, hour=0, minute=0, second=30
            )),
        ],
        [
            InlineKeyboardButton('1 минута', callback_data=delete_time_data.new(
                day=0, hour='0', minute=1, second=0
            )),
            InlineKeyboardButton('10 минут', callback_data=delete_time_data.new(
                day=0, hour='0', minute=10, second=0
            )),
            InlineKeyboardButton('30 минут', callback_data=delete_time_data.new(
                day=0, hour=0, minute=30, second=0
            )),
        ],
        [
            InlineKeyboardButton('1 час', callback_data=delete_time_data.new(
                day=0, hour=1, minute=0, second=0
            )),
            InlineKeyboardButton('2 часа', callback_data=delete_time_data.new(
                day=0, hour=2, minute=0, second=0
            )),
            InlineKeyboardButton('3 часа', callback_data=delete_time_data.new(
                day=0, hour=3, minute=0, second=0
            )),
        ],
        [
            InlineKeyboardButton('6 часов', callback_data=delete_time_data.new(
                day=0, hour=6, minute=0, second=0
            )),
            InlineKeyboardButton('8 часов', callback_data=delete_time_data.new(
                day=0, hour=8, minute=0, second=0
            )),
            InlineKeyboardButton('12 часов', callback_data=delete_time_data.new(
                day=0, hour=12, minute=0, second=0
            )),
        ],
        [
            InlineKeyboardButton('1 день', callback_data=delete_time_data.new(
                day=1, hour=0, minute=0, second=0
            )),
            InlineKeyboardButton('2 дня', callback_data=delete_time_data.new(
                day=2, hour=0, minute=0, second=0
            )),
            InlineKeyboardButton('3 дня', callback_data=delete_time_data.new(
                day=3, hour=0, minute=0, second=0
            )),
        ],
        [
            InlineKeyboardButton('« Назад', callback_data=delete_time_data.new(
                day='back', hour='back', minute='back', second='back'
            )),
        ]
    ]
)
