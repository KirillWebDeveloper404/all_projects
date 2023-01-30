from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

notification_data = CallbackData('notification', 'type', 'club_id', 'day')


async def get_notification_main(club_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton('После покупки', callback_data=notification_data.new(
                    type='after_buy', club_id=club_id, day='0'
                ))
            ],
            [
                InlineKeyboardButton('Уведомление за 3 дня', callback_data=notification_data.new(
                    type='notification', club_id=club_id, day='3'
                ))
            ],
            [
                InlineKeyboardButton('Уведомление за 2 дня', callback_data=notification_data.new(
                    type='notification', club_id=club_id, day='2'
                ))
            ],
            [
                InlineKeyboardButton('Уведомление за 1 день', callback_data=notification_data.new(
                    type='notification', club_id=club_id, day='1'
                ))
            ],
            [
                InlineKeyboardButton('Конец подписки', callback_data=notification_data.new(
                    type='end_subscribe', club_id=club_id, day='0'
                ))
            ],
            [
                InlineKeyboardButton('Назад', callback_data=notification_data.new(
                    type='back', club_id=club_id, day='0'
                ))
            ],
        ]
    )