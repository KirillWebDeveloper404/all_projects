from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

private_club_data = CallbackData('private_club', 'prefix')

private_club_main = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Создать новый', callback_data=private_club_data.new(prefix='new'))
        ],
        [
            InlineKeyboardButton(text='Список', callback_data=private_club_data.new(prefix='list'))
        ],
        [
            InlineKeyboardButton(text='Назад', callback_data=private_club_data.new(prefix='back'))
        ],
    ]
)
