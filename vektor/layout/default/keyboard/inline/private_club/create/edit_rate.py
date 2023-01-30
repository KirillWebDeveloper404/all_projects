from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from .all_datas import add_field_rate_private_club

edit_rate_pr_club = CallbackData('edit_rate_pr_club', 'pr', 'rt_id', 'cl_id')


async def get_edit_rate_main_kb(rate_id, club_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton('Название',
                                 callback_data=add_field_rate_private_club.new(cl_id=club_id, rt_id=rate_id, pr='name')
                                 ),
            InlineKeyboardButton('Описание',
                                 callback_data=add_field_rate_private_club.new(cl_id=club_id, rt_id=rate_id, pr='desk')
                                 ),

        ],
        [
            InlineKeyboardButton('Медиа',
                                 callback_data=add_field_rate_private_club.new(cl_id=club_id, rt_id=rate_id, pr='media')
                                 ),
            InlineKeyboardButton('Демо',
                                 callback_data=add_field_rate_private_club.new(cl_id=club_id, rt_id=rate_id, pr='demo')
                                 ),

        ],
        [
            InlineKeyboardButton('Период',
                                 callback_data=add_field_rate_private_club.new(cl_id=club_id, rt_id=rate_id, pr='time')
                                 ),
            InlineKeyboardButton('Цена',
                                 callback_data=add_field_rate_private_club.new(cl_id=club_id, rt_id=rate_id, pr='price')
                                 ),

        ],
        [
            InlineKeyboardButton('Назад',
                                 callback_data=edit_rate_pr_club.new(rt_id=rate_id, pr='back', cl_id=club_id)
                                 ),
            InlineKeyboardButton('Удалить',
                                 callback_data=edit_rate_pr_club.new(rt_id=rate_id, pr='del', cl_id=club_id)
                                 ),

        ],

    ])
