from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from keyboard.inline.create_message_af.all_data import del_media

msg_photo_af_data = CallbackData('msg_photo_af_data', 'prefix')

async def generate_get_photo_keyboard(data):
    inline_keyboard = []
    if data['photo']:
        inline_keyboard.append([InlineKeyboardButton('Поменять фото', callback_data=msg_photo_af_data.new(
            prefix='change_photo'
        ))])
        inline_keyboard.append([InlineKeyboardButton('Удалить фото', callback_data=del_media.new(pr='None'))])
    inline_keyboard.append([InlineKeyboardButton('« Назад', callback_data=msg_photo_af_data.new(prefix='back'))])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
