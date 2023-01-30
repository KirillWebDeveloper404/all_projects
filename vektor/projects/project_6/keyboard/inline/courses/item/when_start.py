from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

when_start_course_data = CallbackData('when_start_course', 'prefix')

when_start_course = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Мгновенно', callback_data=when_start_course_data.new(prefix='fast')),
        ],
        [
            InlineKeyboardButton(text='Еженедельно', callback_data=when_start_course_data.new(prefix='week')),
        ],
        [
            InlineKeyboardButton(text='Ежемесячно', callback_data=when_start_course_data.new(prefix='month')),
        ],
    ]
)