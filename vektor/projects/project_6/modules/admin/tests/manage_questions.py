from aiogram import types

from keyboard.inline.tests.list import list_tests_data, generate_list_tests_keyboard
from keyboard.inline.tests.manage_question import get_manage_question_keyboard, manage_question_test_data
from loader import dp
from modules.DataBase import get_answers_question, delete_question_test


@dp.callback_query_handler(list_tests_data.filter())
async def back_list_tests(call: types.CallbackQuery, callback_data: dict):
    question_id = callback_data.get('id')
    await call.answer(cache_time=1)
    answers = get_answers_question(question_id)
    if answers:
        question = answers[0].question
        text = f'Вопрос: {question.text}'
        keyboard = await get_manage_question_keyboard(answers=answers, question_id=question_id)
        await call.message.edit_text(text, reply_markup=keyboard)
    else:
        await call.answer(text='У этого вопроса нет вариантов ответа', show_alert=True)


@dp.callback_query_handler(manage_question_test_data.filter(prefix='back'))
async def back_to_list(call: types.CallbackQuery):
    text = 'Выберете квиз'
    keyboard = await generate_list_tests_keyboard()
    await call.answer(cache_time=1)
    await call.message.edit_text(text, reply_markup=keyboard)


@dp.callback_query_handler(manage_question_test_data.filter(prefix='delete'))
async def back_to_list(call: types.CallbackQuery, callback_data: dict):
    question_id = int(callback_data.get('id'))
    await call.answer(cache_time=1)
    delete_question_test(question_id)
    text = 'Выберете квиз'
    keyboard = await generate_list_tests_keyboard()
    await call.message.edit_text(text, reply_markup=keyboard)
