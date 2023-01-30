from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

buy_rate = CallbackData('bbbbuy_rate', 'rate_id', 'pr')


async def buy_rate_kb(rate_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton('Купить', callback_data=buy_rate.new(rate_id=rate_id, pr='item'))
        ],
        [
            InlineKeyboardButton('Назад', callback_data=buy_rate.new(rate_id=rate_id, pr='back'))
        ]
    ])
