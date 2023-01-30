from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

course_data = CallbackData('course_main', 'prefix')

course_main = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Создать новый', callback_data=course_data.new(prefix='new'))
        ],
        [
            InlineKeyboardButton(text='Список', callback_data=course_data.new(prefix='list'))
        ],
        [
            InlineKeyboardButton(text='Назад', callback_data=course_data.new(prefix='back'))
        ],
    ]
)
