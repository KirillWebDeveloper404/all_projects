from aiogram.types import InlineKeyboardButton

from modules.DataBase import get_msgs_by_funnel_id_and_type


async def get_system_messages_af_kb(funnel_id):
    msgs = get_msgs_by_funnel_id_and_type('system', funnel_id=funnel_id)
    inline_keyboard = []
    for msg in msgs:
        inline_keyboard.append([InlineKeyboardButton(f'За {msg.day} в {msg.hour}:{msg.minute}')])
    inline_keyboard.append([InlineKeyboardButton(f'« Назад')])
