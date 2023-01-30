from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

manage_answer_test_data = CallbackData('manage_answer_test_data', 'id', 'prefix')


async def get_manage_answer_test_keyboard(answer_id):
    inline_keyboard = [
        [
            InlineKeyboardButton(text='Редактировать', callback_data=manage_answer_test_data.new(id=answer_id, prefix='edit'))
        ],
        [
            InlineKeyboardButton(text='Удалить', callback_data=manage_answer_test_data.new(id=answer_id, prefix='delete'))
        ],
        [
            InlineKeyboardButton(text='« Назад', callback_data=manage_answer_test_data.new(id=answer_id, prefix='back'))
        ],

    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
