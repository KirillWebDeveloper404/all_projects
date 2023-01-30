from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from .all_data import back_for_edit, delete_something

edit_gif_msg_data = CallbackData('edit_gif_msg_data', 'prefix')


async def generate_get_gif_keyboard(data):
    inline_keyboard = []
    if data['gif']:
        inline_keyboard.append([InlineKeyboardButton('Поменять гифку', callback_data=edit_gif_msg_data.new(
            prefix='change'
        ))])
        inline_keyboard.append([InlineKeyboardButton('Удалить гифку', callback_data=delete_something.new(prefix='gif'))])
    inline_keyboard.append([InlineKeyboardButton('« Назад', callback_data=back_for_edit.new(p='1'))])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

