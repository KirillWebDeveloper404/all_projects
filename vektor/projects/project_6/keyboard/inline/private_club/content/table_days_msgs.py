import math

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from modules.DataBase import get_max_day_message

table_days_msgs_dt = CallbackData('table_days_msgs', 'day', 'cl_id', 'pr')


async def get_table_days_msgs_kb(club_id, step=1):
    days = get_max_day_message(club_id)
    if not days:
        return None
    one_step = 35
    one_line = 7
    inline_keyboard = []
    is_slide = days > one_step

    if step > 1:
        use_days = days - one_step * (step - 1)
        start = one_step * (step - 1) + 1
    else:
        if is_slide:
            use_days = 35
        else:
            use_days = days
        start = 1
    line_count = math.ceil(use_days / one_line)
    end = start + line_count * one_line


    row = []
    for i in range(start, end):
        if i <= days:
            row.append(InlineKeyboardButton(f'{i}', callback_data=table_days_msgs_dt.new(
                day=i, cl_id=club_id, pr='day'
            )))
        else:
            row.append(InlineKeyboardButton(' ', callback_data=table_days_msgs_dt.new(day=i, cl_id=club_id, pr='null')))
        if i % 7 == 0:
            inline_keyboard.append(row)
            row = []

    if is_slide:
        row = []
        if step > 1:
            row.append(InlineKeyboardButton('«', callback_data=table_days_msgs_dt.new(
                day=step, cl_id=club_id, pr='prev'
            )))
        row.append(
            InlineKeyboardButton('»', callback_data=table_days_msgs_dt.new(
                day=step, cl_id=club_id, pr='next'
            )),
        )
        inline_keyboard.append(row)

    inline_keyboard.append([InlineKeyboardButton('Назад', callback_data=table_days_msgs_dt.new(
        day=step, cl_id=club_id, pr='back'
    ))])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


