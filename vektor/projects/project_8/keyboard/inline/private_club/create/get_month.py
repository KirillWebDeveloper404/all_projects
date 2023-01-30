from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

month_time_dt = CallbackData('month_time_dt', 'month')

month_time = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='1', callback_data=month_time_dt.new(month='1')),
            InlineKeyboardButton(text='2', callback_data=month_time_dt.new(month='2')),
            InlineKeyboardButton(text='3', callback_data=month_time_dt.new(month='3'))
        ],
        [
            InlineKeyboardButton(text='4', callback_data=month_time_dt.new(month='4')),
            InlineKeyboardButton(text='5', callback_data=month_time_dt.new(month='5')),
            InlineKeyboardButton(text='6', callback_data=month_time_dt.new(month='6'))
        ],
        [
            InlineKeyboardButton(text='7', callback_data=month_time_dt.new(month='7')),
            InlineKeyboardButton(text='8', callback_data=month_time_dt.new(month='8')),
            InlineKeyboardButton(text='9', callback_data=month_time_dt.new(month='9'))
        ],
        [
            InlineKeyboardButton(text='10', callback_data=month_time_dt.new(month='10')),
            InlineKeyboardButton(text='11', callback_data=month_time_dt.new(month='11')),
            InlineKeyboardButton(text='12', callback_data=month_time_dt.new(month='12'))
        ],

    ]
)