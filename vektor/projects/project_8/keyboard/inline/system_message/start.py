from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

system_message_data = CallbackData('system_message_data', 'prefix')

system_message_main = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='О школе', callback_data=system_message_data.new(prefix='school')),
        InlineKeyboardButton(text='Помощь', callback_data=system_message_data.new(prefix='help'))

    ],
    [
        InlineKeyboardButton(text='« Назад', callback_data=system_message_data.new(prefix='back'))
    ],
])