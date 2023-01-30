from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline.create_test import create_result_msg_keyboard
from loader import dp
from modules.DataBase import create_answer
from states import AddTest


@dp.message_handler(state=AddTest.get_answer)
async def process_qet_question_test(message: types.Message, state: FSMContext):
    answer_text = message.text
    text = f'Ответ: {answer_text}\n\n' \
           f'Добавьте сообщение которое будет отправляться пользователю после ответа на этот вопрос\n\n' \
           f'Если ответа нет, то пропустите.'
    data = await state.get_data()
    answer = create_answer(data['question_id'], answer_text)
    await state.update_data(data={
        'answer': answer_text,
        'answer_id': answer.id
    })
    data = await state.get_data()

    keyboard = await create_result_msg_keyboard(data)
    await message.answer(text, reply_markup=keyboard)
    await AddTest.create_result.set()