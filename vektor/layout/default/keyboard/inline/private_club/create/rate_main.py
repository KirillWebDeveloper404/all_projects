from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

private_club_rate_data = CallbackData('pr_club_rates', 'cl_id', 'pr')


async def get_private_club_rate_main(club_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Список тарифов',
                callback_data=private_club_rate_data.new(cl_id=club_id, pr='list')
                                 )
        ],
        [
            InlineKeyboardButton(
                text='Добавить новый тариф',
                callback_data=private_club_rate_data.new(cl_id=club_id, pr='new_rate')
            )
        ],
        [
            InlineKeyboardButton(
                text='Назад',
                callback_data=private_club_rate_data.new(cl_id=club_id, pr='back')
            )
        ],
    ])
