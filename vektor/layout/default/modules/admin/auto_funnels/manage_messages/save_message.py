from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline import manage_messages
from keyboard.inline.edit.edit_message import edit_message_kb_data
from keyboard.inline.tests.manage_answer import get_manage_answer_test_keyboard
from loader import dp
from modules.DataBase import save_new_message_af, save_new_result_test, get_message_af_by_id, get_question_by_id
from states import EditMessages
from utils.functions import has_text_youtube_link


@dp.callback_query_handler(edit_message_kb_data.filter(prefix='save'), state=EditMessages.start)
async def save_message(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    data = await state.get_data()
    if data['type_message'] == 'system' or data['type_message'] == 'content':
        message = save_new_message_af(
            message_id=data['message_id'],
            message_text=data['text'],
            photo=data['photo'],
            gif=data['gif'],
            video=data['video'],
            voice=data['voice'],
            video_note=data['video_note'],
            document=data['document'],
            audio=data['audio'],
            day=data['send_day'],
            hour=data['send_hour'],
            minute=data['send_minute'],
            interval_msg_id=data['interval_msg'],
            interval_hour=data['interval_hour'],
            interval_minute=data['interval_minute'],
            interval_day=data['interval_day'],
            interval_second=data['interval_second'],
            delete_hour=data['delete_hour'],
            delete_day=data['delete_day'],
            delete_second=data['delete_second'],
            delete_minute=data['delete_minute'],
            link=data['link'],
            text_link=data['text_link'],
            test=data['test']
        )
        message = get_message_af_by_id(message.id)
        await call.answer(cache_time=1)
        keyboard = await manage_messages(message.auto_funnel_id)
        await call.message.answer('Управление сообщениями в воронке', reply_markup=keyboard)
    else:
        result = save_new_result_test(
            message_id=data['message_id'],
            result_text=data['text'],
            photo=data['photo'],
            gif=data['gif'],
            video=data['video'],
            voice=data['voice'],
            video_note=data['video_note'],
            document=data['document'],
            audio=data['audio'],
            link=data['link'],
            text_link=data['text_link'],
            test=data['test']
        )
        keyboard = await get_manage_answer_test_keyboard(result.answer)
        await get_result_message(call, result, keyboard)
    await call.message.delete()
    await state.finish()


async def get_result_message(call, result, keyboard):
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
