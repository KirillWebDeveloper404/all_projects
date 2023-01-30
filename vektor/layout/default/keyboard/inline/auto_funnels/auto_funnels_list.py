from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from modules.DataBase import get_all_auto_funnels

auto_funnels_list_data = CallbackData('auto_funnels_list', 'id', 'prefix')


async def generate_list_auto_funnels() -> InlineKeyboardMarkup:
    inline_keyboard = []
    auto_funnels = get_all_auto_funnels()
    for auto_funnel in auto_funnels:
        inline_keyboard.append([InlineKeyboardButton(text=f'{auto_funnel.name}',
                                                     callback_data=auto_funnels_list_data.new(id=f'{auto_funnel.id}',
                                                                                              prefix='auto_funnels'))])
    inline_keyboard.append([InlineKeyboardButton(text='Создать новую',
                                                 callback_data=auto_funnels_list_data.new(id='None', prefix='create'))])

    inline_keyboard.append([InlineKeyboardButton(text='« Назад',
                                                 callback_data=auto_funnels_list_data.new(id='None', prefix='back'))])

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
