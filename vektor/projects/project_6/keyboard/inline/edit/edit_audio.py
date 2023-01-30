from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from .all_data import back_for_edit, delete_something

edit_audio_msg_data = CallbackData('edit_audio_msg_data', 'prefix')


async def generate_get_audio_keyboard(data):
    inline_keyboard = []
    if data['audio']:
        inline_keyboard.append([InlineKeyboardButton('Поменять аудио', callback_data=edit_audio_msg_data.new(
            prefix='change'
        ))])
        inline_keyboard.append([InlineKeyboardButton('Удалить аудио', callback_data=delete_something.new(prefix='audio'))])
    inline_keyboard.append([InlineKeyboardButton('« Назад', callback_data=back_for_edit.new(p='1'))])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
