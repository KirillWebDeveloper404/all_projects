from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from .all_data import delete_something

msg_text_af_data = CallbackData('msg_text_af', 'prefix')


async def generate_get_text_keyboard(data):
    inline_keyboard = []
    if data['text']:
        inline_keyboard.append([InlineKeyboardButton('Поменять текст', callback_data=msg_text_af_data.new(
            prefix='change_text'
        ))])
        inline_keyboard.append([InlineKeyboardButton('Удалить текст', callback_data=delete_something.new(
            thing='text'
        ))])
    inline_keyboard.append([InlineKeyboardButton('« Назад', callback_data=msg_text_af_data.new(prefix='back'))])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
