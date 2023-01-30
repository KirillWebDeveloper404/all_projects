from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline.tests.manage_answer import get_manage_answer_test_keyboard, manage_answer_test_data
from keyboard.inline.tests.manage_question import manage_question_test_data, get_manage_question_keyboard
from loader import dp
from modules.DataBase import get_result_by_answer_id, get_question_by_id, get_answers_question, get_answers_by_id, \
    delete_answer
from states import EditMessages
from utils.functions import has_text_youtube_link
from utils.functions.edit_messages_msg import get_text_edit_messages


@dp.callback_query_handler(manage_answer_test_data.filter(prefix='back'))
async def back_to_list(call: types.CallbackQuery, callback_data: dict):
    answer_id = int(callback_data.get('id'))
    answer = get_answers_by_id(answer_id)
    text = f'Вопрос: {answer.question.text}'
    answers = get_answers_question(answer.question.id)
    keyboard = await get_manage_question_keyboard(answers=answers, question_id=answer.question.id)
    await call.message.delete()
    await call.message.answer(text, reply_markup=keyboard)
    await call.answer(cache_time=1)


@dp.callback_query_handler(manage_answer_test_data.filter(prefix='delete'))
async def back_to_list(call: types.CallbackQuery, callback_data: dict):
    answer_id = int(callback_data.get('id'))
    answer = get_answers_by_id(answer_id)
    text = f'Вопрос: {answer.question.text}'
    delete_answer(answer_id)
    answers = get_answers_question(answer.question.id)
    keyboard = await get_manage_question_keyboard(answers=answers, question_id=answer.question.id)
    await call.message.delete()
    await call.message.answer(text, reply_markup=keyboard)


@dp.callback_query_handler(manage_answer_test_data.filter(prefix='edit'))
async def back_to_list(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=1)
    answer_id = callback_data.get('id')
    message = get_result_by_answer_id(answer_id)

    data = {
        'message_id': message.id,
        'type_message': 'test',
        'photo': message.photo,
        'gif': message.gif,
        'document': message.document,
        'video': message.video,
        'video_note': message.video_note,
        'voice': message.voice,
        'audio': message.audio,
        'text': message.result_text,
        'text_link': message.text_link,
        'link': message.link,
        'delete_second': None,
        'delete_minute': None,
        'delete_hour': None,
        'delete_day': None,
        'send_day': None,
        'send_hour': None,
        'send_minute': None,
        'is_first': None,
        'interval_msg': None,
        'interval_second': None,
        'interval_minute': None,
        'interval_hour': None,
        'interval_day': None,
        'test': message.test,
    }

    await EditMessages.start.set()
    await state.update_data(data=data)
    await get_text_edit_messages(data, call.message)


@dp.callback_query_handler(manage_question_test_data.filter())
async def back_to_list(call: types.CallbackQuery, callback_data: dict):
    answer_id = callback_data.get('id')
    keyboard = await get_manage_answer_test_keyboard(answer_id)
    await send_answer_by_id(answer_id, call, keyboard)


async def send_answer_by_id(answer_id, call: types.CallbackQuery, keyboard=None):
    result = get_result_by_answer_id(answer_id)
    if result:
        await call.answer(cache_time=1)
        has_youtube = await has_text_youtube_link(result.result_text)
        if result.result_text:
            text = 'Сообщение:\n' \
                   f'{result.result_text}\n\n'
        else:
            text = 'Сообщение:\n' \
                   '<Пустое сообщение>\n\n'

        text += '====================\n'
        if result.link:
            text += 'Кнопка:\n' \
                    f'Ссылка: {result.link}\n' \
                    f'Текст: {result.text_link}\n\n'
        else:
            text += 'Кнопка:Отстутствует\n\n'

        if result.test:
            question = get_question_by_id(result.test)
            if question:
                text += f'Редирект на вопрос: {question.text}'
            else:
                text += f'Редирект на удаленный вопрос т.е. отправлен не будет'
        else:
            text += f'Редирект на вопрос: отсутствует'

        if result.photo:
            if has_youtube:
                await call.message.answer_photo(photo=result.photo)
                await call.message.answer(text=text, reply_markup=keyboard)
            else:
                await call.message.answer_photo(photo=result.photo, caption=text, reply_markup=keyboard)
        elif result.gif:
            if has_youtube:
                await call.message.answer_animation(animation=result.gif)
                await call.message.answer(text=text, reply_markup=keyboard)
            else:
                await call.message.answer_animation(animation=result.gif, caption=text,
                                                    reply_markup=keyboard)
        elif result.audio:
            if has_youtube:
                await call.message.answer_audio(audio=result.audio)
                await call.message.answer(text=text, reply_markup=keyboard)
            else:
                await call.message.answer_audio(audio=result.audio, caption=text, reply_markup=keyboard)
        elif result.document:
            if has_youtube:
                await call.message.answer_document(document=result.document)
                await call.message.answer(text=text, reply_markup=keyboard)
            else:
                await call.message.answer_document(document=result.document, caption=text,
                                                   reply_markup=keyboard)
        elif result.video:
            if has_youtube:
                await call.message.answer_video(video=result.video)
                await call.message.answer(text=text, reply_markup=keyboard)
            else:
                await call.message.answer_video(video=result.video, caption=text, reply_markup=keyboard)
        elif result.voice:
            await call.message.answer_voice(voice=result.voice)
            await call.message.answer(text=text, reply_markup=keyboard)
        elif result.video_note:
            await call.message.answer_video_note(video_note=result.video_note)
            await call.message.answer(text=text, reply_markup=keyboard)
        else:
            if result.result_text:
                await call.message.answer(text=result.result_text, reply_markup=keyboard)



    else:
        await call.answer('Этот ответ пустой!', show_alert=True)
