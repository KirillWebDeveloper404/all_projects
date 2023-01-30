from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from modules.DataBase import get_msgs_by_funnel_id_and_type_without_interval

reference_interval_msgs_data = CallbackData('reference_interval_msgs', 'msg_id')
msg_interval_data = CallbackData('msg_interval_data', 'prefix')


async def get_keyboard_for_interval_msgs(data):
    msgs = get_msgs_by_funnel_id_and_type_without_interval('content', data['funnel_id'])
    if len(msgs) < 1:
        return None
    inline_keyboard = []
    for msg in msgs:
        print(msg)
        if msg.is_first:
            inline_keyboard.append(
                [InlineKeyboardButton('Первое сообщение', callback_data=reference_interval_msgs_data.new(
                    msg_id=msg.id
                ))])
        else:
            inline_keyboard.append([InlineKeyboardButton(f'день {msg.day} в {msg.hour}:{msg.minute}',
                                                        callback_data=reference_interval_msgs_data.new(msg_id=msg.id))])
    inline_keyboard.append([InlineKeyboardButton('« Назад', callback_data=msg_interval_data.new(prefix='back'))])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
