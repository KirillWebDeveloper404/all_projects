from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

manage_private_club_data = CallbackData('manage_pr_cl_dt', 'club_id', 'pr')

async def manage_private_club_main(club_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Название', callback_data=manage_private_club_data.new(club_id=club_id, pr='name')
            ),
            InlineKeyboardButton(
                text='Тарифы', callback_data=manage_private_club_data.new(club_id=club_id, pr='rate')
            ),
        ],
        [

            InlineKeyboardButton(
                text='Контент', callback_data=manage_private_club_data.new(club_id=club_id, pr='content')
            ),
            InlineKeyboardButton(
                text='Сообщество', callback_data=manage_private_club_data.new(club_id=club_id, pr='community')
            ),
        ],
        [

            InlineKeyboardButton(
                text='Сообщения', callback_data=manage_private_club_data.new(club_id=club_id, pr='messages')
            ),
            InlineKeyboardButton(
                text='Удалить', callback_data=manage_private_club_data.new(club_id=club_id, pr='delete')
            )
        ],
        [
            InlineKeyboardButton(
                text='Назад', callback_data=manage_private_club_data.new(club_id=club_id, pr='back')
            )
        ],

    ])

