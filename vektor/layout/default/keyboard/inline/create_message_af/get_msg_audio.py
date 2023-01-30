from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from keyboard.inline.create_message_af.all_data import del_media

msg_audio_af_data = CallbackData('msg_audio_af_data', 'prefix')

async def generate_get_audio_keyboard(data):
    inline_keyboard = []
    if data['audio']:
        inline_keyboard.append([InlineKeyboardButton('Поменять аудио', callback_data=msg_audio_af_data.new(
            prefix='change_audio'
        ))])
        inline_keyboard.append([InlineKeyboardButton('Удалить аудио', callback_data=del_media.new(pr='None'))])
    inline_keyboard.append([InlineKeyboardButton('« Назад', callback_data=msg_audio_af_data.new(prefix='back'))])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
