from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from modules.DataBase import create_question
from states import AddTest


@dp.message_handler(state=AddTest.get_question)
async def process_qet_question_test(message: types.Message, state: FSMContext):
    question_text = message.text
    question = create_question(question_text)
    await state.update_data(data={
        'question_text': question_text,
        'question_id': question.id
    })
    await AddTest.get_answer.set()
    await message.answer('Добавьте ответ:')
