from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from modules.DataBase import get_segment_products, get_not_deleted_products, get_all_auto_funnels

segment_data = CallbackData('segment_data', 'prefix')


async def get_segment_keyboard():
    admin_mailing = InlineKeyboardMarkup(row_width=2)
    admin_mailing.row(
        InlineKeyboardButton("Всем пользователям", callback_data=segment_data.new(prefix="all")),
    )
    for funnel in get_all_auto_funnels():
        admin_mailing.row(
            InlineKeyboardButton(f"воронка {funnel.name}", callback_data=segment_data.new(prefix=f"funnel_{funnel.id}"))
        )

    admin_mailing.row(InlineKeyboardButton("« Назад", callback_data=segment_data.new(prefix="back")))

    return admin_mailing
