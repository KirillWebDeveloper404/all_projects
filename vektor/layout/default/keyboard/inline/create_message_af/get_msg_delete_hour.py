from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from keyboard.inline.create_message_af.all_data import delete_something

msg_delete_hour_data = CallbackData('msg_delete_hour_data', 'prefix')


async def generate_get_delete_hour_keyboard(data):
    inline_keyboard = []
    if data['delete_hour'] or data['delete_minute'] or data['delete_second'] or data['delete_day']:
        inline_keyboard.append([InlineKeyboardButton('Поменять время удаления', callback_data=msg_delete_hour_data.new(
            prefix='change_delete_hour'
        ))])
        inline_keyboard.append([InlineKeyboardButton('Удалить время удаления', callback_data=delete_something.new(
            thing='delete_timer'
        ))])
    inline_keyboard.append([InlineKeyboardButton('« Назад', callback_data=msg_delete_hour_data.new(prefix='back'))])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
