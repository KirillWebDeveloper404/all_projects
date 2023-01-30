from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.callback_data import CallbackData

manage_question_test_data = CallbackData('manage_question_tests_data', 'id', 'prefix')


async def get_manage_question_keyboard(answers: List, question_id='None'):
    inline_keyboard = []
    for answer in answers:
        inline_keyboard.append(
            [InlineKeyboardButton(text=answer.text,
                                  callback_data=manage_question_test_data.new(id=answer.id, prefix='answer'))]
        )

    inline_keyboard.append([InlineKeyboardButton(text='Удалить вопрос',
                                                 callback_data=manage_question_test_data.new(id=question_id, prefix='delete'))])
    inline_keyboard.append(
        [InlineKeyboardButton(text='« Назад', callback_data=manage_question_test_data.new(id=question_id, prefix='back'))])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
