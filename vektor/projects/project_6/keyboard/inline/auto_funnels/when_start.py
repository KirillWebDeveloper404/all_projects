from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

when_start_data = CallbackData('when_start_funnel', 'prefix')

when_start = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Мгновенно', callback_data=when_start_data.new(prefix='fast')),
        ],
        [
            InlineKeyboardButton(text='Еженедельно', callback_data=when_start_data.new(prefix='week')),
        ],
        [
            InlineKeyboardButton(text='Ежемесячно', callback_data=when_start_data.new(prefix='month')),
        ],
    ]
)