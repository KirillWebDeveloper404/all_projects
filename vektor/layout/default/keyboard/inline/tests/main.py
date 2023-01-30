from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

test_main_data = CallbackData('test_main_data', 'prefix')

test_main = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton('Создать новый', callback_data=test_main_data.new(prefix='new'))
        ],
        [
            InlineKeyboardButton('Список', callback_data=test_main_data.new(prefix='list'))
        ],
        [
            InlineKeyboardButton('« Назад', callback_data=test_main_data.new(prefix='back'))
        ],
    ]
)