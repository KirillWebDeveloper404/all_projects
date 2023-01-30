from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from .all_data import delete_something
from keyboard.inline.edit.all_data import back_for_edit

edit_delete = CallbackData('edit_delete', 'prefix')


async def generate_edit_delete_keyboard(data):
    inline_keyboard = []
    if data['delete_hour'] or data['delete_minute'] or data['delete_second'] or data['delete_day']:
        inline_keyboard.append([InlineKeyboardButton('Поменять время удаления', callback_data=edit_delete.new(
            prefix='change'
        ))])
        inline_keyboard.append([InlineKeyboardButton('Удалить время удаления', callback_data=delete_something.new(
            prefix='delete'
        ))])
    inline_keyboard.append([InlineKeyboardButton('« Назад', callback_data=back_for_edit.new(p='1'))])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
