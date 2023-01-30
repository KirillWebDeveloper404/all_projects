from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from modules.DataBase import get_all_content_messages_by_funnel_id
from .all_datas import create_new_message_af_ff

content_message = CallbackData('content_message_data', 'message_id', 'funnel_id')


async def get_all_content_messages_kb(funnel_id):
    messages_funnel = get_all_content_messages_by_funnel_id(funnel_id)
    inline_keyboard = []
    for i in range(len(messages_funnel)):
        inline_keyboard.append(
            [InlineKeyboardButton(text=f'Сообщение {i + 1}', callback_data=content_message.new(
                message_id=messages_funnel[i].id, funnel_id=funnel_id
            ))])
    inline_keyboard.append([InlineKeyboardButton('Добавить сообщение', callback_data=create_new_message_af_ff.new(
        msg_type='content', funnel_id=funnel_id, edit='yes'))
                            ])
    inline_keyboard.append([InlineKeyboardButton('« Назад', callback_data=content_message.new(
        message_id='None', funnel_id=funnel_id))
                            ])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
