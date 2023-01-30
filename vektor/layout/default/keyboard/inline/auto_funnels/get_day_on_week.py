from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

day_on_week_data = CallbackData('day_on_week', 'day')
day_on_week = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Понедельник', callback_data=day_on_week_data.new(day='0'))
        ],
        [
            InlineKeyboardButton(text='Вторник', callback_data=day_on_week_data.new(day='1'))
        ],
        [
            InlineKeyboardButton(text='Среда', callback_data=day_on_week_data.new(day='2'))
        ],
        [
            InlineKeyboardButton(text='Четверг', callback_data=day_on_week_data.new(day='3'))
        ],
        [
            InlineKeyboardButton(text='Пятница', callback_data=day_on_week_data.new(day='4'))
        ],
        [
            InlineKeyboardButton(text='Суббота', callback_data=day_on_week_data.new(day='5'))
        ],
        [
            InlineKeyboardButton(text='Воскресенье', callback_data=day_on_week_data.new(day='6'))
        ],
    ]
)