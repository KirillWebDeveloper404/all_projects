from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from modules.DataBase import get_all_auto_funnels, get_auto_funnel_by_id

auto_funnels_manage_data = CallbackData('auto_funnels_manage', 'id', 'prefix')


async def generate_auto_funnels_manage(id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton('Сообщения', callback_data=auto_funnels_manage_data.new(id=id, prefix='messages'))
            ],
            [
                InlineKeyboardButton('Удалить воронку',
                                     callback_data=auto_funnels_manage_data.new(id=id, prefix='delete'))
            ],
            [
                InlineKeyboardButton('« Назад', callback_data=auto_funnels_manage_data.new(id=id, prefix='back'))
            ],
        ]
    )
