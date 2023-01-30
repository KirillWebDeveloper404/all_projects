from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

msg_pr_cl = CallbackData('__msg_pr_cl__', 'msg_id', 'cl_id', 'pr', 'day')

async def get_msg_pr_cl_kb(club_id, msg_id, day):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Изменить', callback_data=msg_pr_cl.new(
                msg_id=msg_id, cl_id=club_id, pr='edit', day=day
            ))
        ],
        [
            InlineKeyboardButton(text='Удалить', callback_data=msg_pr_cl.new(
                msg_id=msg_id, cl_id=club_id, pr='del', day=day
            ))
        ],
        [
            InlineKeyboardButton(text='Назад', callback_data=msg_pr_cl.new(
                msg_id=msg_id, cl_id=club_id, pr='back', day=day
            ))
        ],
    ])