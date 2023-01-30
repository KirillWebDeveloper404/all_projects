from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

day_demo_data = CallbackData('day_demo', 'day')

day_demo = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='1 день', callback_data=day_demo_data.new(day='1')),
        InlineKeyboardButton(text='2 дня', callback_data=day_demo_data.new(day='2')),
        InlineKeyboardButton(text='3 дня', callback_data=day_demo_data.new(day='3')),
    ],
    [
        InlineKeyboardButton(text='4 дня', callback_data=day_demo_data.new(day='4')),
        InlineKeyboardButton(text='5 дней', callback_data=day_demo_data.new(day='5')),
        InlineKeyboardButton(text='6 дней', callback_data=day_demo_data.new(day='6')),
    ],
    [
        InlineKeyboardButton(text='7 дней', callback_data=day_demo_data.new(day='7')),
        InlineKeyboardButton(text='8 дней', callback_data=day_demo_data.new(day='8')),
        InlineKeyboardButton(text='9 дней', callback_data=day_demo_data.new(day='9')),
    ],
    [
        InlineKeyboardButton(text='10 дней', callback_data=day_demo_data.new(day='10')),
        InlineKeyboardButton(text='11 дней', callback_data=day_demo_data.new(day='11')),
        InlineKeyboardButton(text='12 дней', callback_data=day_demo_data.new(day='12')),
    ],
    [
        InlineKeyboardButton(text='13 дней', callback_data=day_demo_data.new(day='13')),
        InlineKeyboardButton(text='14 дней', callback_data=day_demo_data.new(day='14')),
        InlineKeyboardButton(text='15 дней', callback_data=day_demo_data.new(day='15')),
    ],
    [
        InlineKeyboardButton(text='0 дней', callback_data=day_demo_data.new(day='0'))
    ]
])