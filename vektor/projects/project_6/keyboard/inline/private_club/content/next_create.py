from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

next_msg_pr_cl_data = CallbackData('next_msg_pr_cl_data', 'pr', 'last_day', 'cl_id')


async def next_message_create(last_day, club_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton('Добавить еще один урок',
                                     callback_data=next_msg_pr_cl_data.new(pr='new', last_day=last_day, cl_id=club_id))
            ],
            [
                InlineKeyboardButton('Перейти к следующему дню',
                                     callback_data=next_msg_pr_cl_data.new(pr='next', last_day=last_day, cl_id=club_id))
            ],
            [
                InlineKeyboardButton('Закончить добавление',
                                     callback_data=next_msg_pr_cl_data.new(pr='cancel', last_day=last_day,
                                                                           cl_id=club_id))
            ],
        ]
    )
