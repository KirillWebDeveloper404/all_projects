from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

main_question_kb_dt = CallbackData('main_question_kb_dt', 'prefix')


main_question_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton('Добавьте еще один ответ', callback_data=main_question_kb_dt.new(
                prefix='add_new'
            ))
        ],
        [
            InlineKeyboardButton('Закончить создание вопроса', callback_data=main_question_kb_dt.new(
                prefix='close'
            ))
        ],
    ]
)