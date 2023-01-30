from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

manage_message_af_kb_data = CallbackData('manage_message_kb_data', 'prefix', 'message_id')


async def get_manage_messages_keyboard(message_id, type):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton('Редактировать',
                                 callback_data=manage_message_af_kb_data.new(prefix='edit', message_id=message_id))
        ],
        [
            InlineKeyboardButton('Удалить',
                                 callback_data=manage_message_af_kb_data.new(prefix='delete', message_id=message_id))
        ],
        [
            InlineKeyboardButton('« Назад',
                                 callback_data=manage_message_af_kb_data.new(prefix=f'{type}_back', message_id=message_id))
        ],
    ])
