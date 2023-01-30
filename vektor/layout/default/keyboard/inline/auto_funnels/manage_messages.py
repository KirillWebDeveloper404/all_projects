from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from modules.DataBase import get_auto_funnel_by_id

auto_funnels_manage_messages_data = CallbackData('funnels_manage_messages', 'id', 'prefix')


async def manage_messages(funnel_id):
    funnel = get_auto_funnel_by_id(funnel_id)
    inline_keyboard = []
    inline_keyboard.append([
                InlineKeyboardButton(text='Первое сообщение',
                                     callback_data=auto_funnels_manage_messages_data.new(id=funnel_id, prefix='first'))
            ])
    if not funnel.fast_start:
        inline_keyboard.append([
            InlineKeyboardButton(text='Системные сообщения',
                                 callback_data=auto_funnels_manage_messages_data.new(id=funnel_id, prefix='system'))
        ])
    inline_keyboard.append([
                InlineKeyboardButton(text='Контент сообщения',
                                     callback_data=auto_funnels_manage_messages_data.new(id=funnel_id, prefix='content'))
            ])

    inline_keyboard.append([
                InlineKeyboardButton(text='« Назад',
                                     callback_data=auto_funnels_manage_messages_data.new(id=funnel_id, prefix='back'))
            ])
    return InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )
