from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from .all_data import delete_something, back_for_edit

msg_button_data = CallbackData('msg_button_data', 'prefix')


async def generate_edit_button(data):
    inline_keyboard = []
    if data['link'] and data['text_link']:
        inline_keyboard.append([InlineKeyboardButton('Поменять кнопку', callback_data=msg_button_data.new(
            prefix='change'
        ))])
        inline_keyboard.append([InlineKeyboardButton('Удалить кнопку', callback_data=delete_something.new(
            prefix='link%%text_link'
        ))])

    inline_keyboard.append([InlineKeyboardButton('« Назад', callback_data=back_for_edit.new(p='1'))])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)