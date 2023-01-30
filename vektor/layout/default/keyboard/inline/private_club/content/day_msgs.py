from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from modules.DataBase import get_day_messages

msgs_pr_cl_data = CallbackData('msgs_pr_cl_data_ff', 'msg_id', 'cl_id', 'day', 'pr')


async def get_day_msgs_pr_cl_kb(club_id, day):
    inline_keyboard = []
    messages = get_day_messages(club_id=club_id, day=day)

    for message in messages:
        inline_keyboard.append([
            InlineKeyboardButton(f'Сообщение {message.hour}:00', callback_data=msgs_pr_cl_data.new(
                msg_id=message.id, cl_id=club_id, day=message.day, pr='item'
            ))
        ])
    inline_keyboard.append([
        InlineKeyboardButton(f'Добавить новое', callback_data=msgs_pr_cl_data.new(
            msg_id='0', cl_id=club_id, day=day, pr='new'
        ))
    ])
    inline_keyboard.append([
        InlineKeyboardButton(f'Назад', callback_data=msgs_pr_cl_data.new(
            msg_id='0', cl_id=club_id, day=day, pr='back'
        ))
    ])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)