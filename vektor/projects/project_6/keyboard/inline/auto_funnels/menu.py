from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

auto_funnels_menu_data = CallbackData('auto_funnels_menu', 'prefix')

auto_funnels_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton('Создать новую', callback_data=auto_funnels_menu_data.new(prefix='create_new'))
        ],
        [
            InlineKeyboardButton('Список автоворонок', callback_data=auto_funnels_menu_data.new(prefix='list'))
        ],
        [
            InlineKeyboardButton('Запуск воронок', callback_data=auto_funnels_menu_data.new(prefix='play'))
        ],
        [
            InlineKeyboardButton('Архив', callback_data=auto_funnels_menu_data.new(prefix='archive'))
        ],
        [
            InlineKeyboardButton('« Назад', callback_data=auto_funnels_menu_data.new(prefix='back'))
        ],

    ]
)