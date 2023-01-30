from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import keyboard
from keyboard.inline.tests.call_datas import answer_test_dt
from loader import dp
from modules.DataBase import get_result_by_answer_id, get_question_by_id, get_answers_question, \
    register_user_result_test
from utils.functions import has_text_youtube_link


@dp.callback_query_handler(answer_test_dt.filter())
async def process_add_result(call: types.CallbackQuery, callback_data: dict):
    answer_id = callback_data.get('id')
    result = get_result_by_answer_id(answer_id)
    await call.message.delete()
    register_user_result_test(call.from_user.id, result.id)
    if result:
        await call.answer(cache_time=1)
        has_youtube = await has_text_youtube_link(result.result_text)
        if result.link:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text=result.text_link, url=result.link)]])
        else:
            keyboard = None

        if result.photo:
            if has_youtube:
                await call.message.answer_photo(photo=result.photo)
                if result.result_text:
                    await call.message.answer(text=result.result_text, reply_markup=keyboard)
            else:
                await call.message.answer_photo(photo=result.photo, caption=result.result_text, reply_markup=keyboard)
        elif result.gif:
            if has_youtube:
                await call.message.answer_animation(animation=result.gif)
                if result.result_text:
                    await call.message.answer(text=result.result_text, reply_markup=keyboard)
            else:
                await call.message.answer_animation(animation=result.gif, caption=result.result_text,
                                                    reply_markup=keyboard)
        elif result.audio:
            if has_youtube:
                await call.message.answer_audio(audio=result.audio)
                if result.result_text:
                    await call.message.answer(text=result.result_text, reply_markup=keyboard)
            else:
                await call.message.answer_audio(audio=result.audio, caption=result.result_text, reply_markup=keyboard)
        elif result.document:
            if has_youtube:
                await call.message.answer_document(document=result.document)
                if result.result_text:
                    await call.message.answer(text=result.result_text, reply_markup=keyboard)
            else:
                await call.message.answer_document(document=result.document, caption=result.result_text,
                                                   reply_markup=keyboard)
        elif result.video:
            if has_youtube:
                await call.message.answer_video(video=result.video)
                if result.result_text:
                    await call.message.answer(text=result.result_text, reply_markup=keyboard)
            else:
                await call.message.answer_video(video=result.video, caption=result.result_text, reply_markup=keyboard)
        elif result.voice:
            await call.message.answer_voice(voice=result.voice)
            if result.result_text:
                await call.message.answer(text=result.result_text, reply_markup=keyboard)
        elif result.video_note:
            await call.message.answer_video_note(video_note=result.video_note)
            if result.result_text:
                await call.message.answer(text=result.result_text, reply_markup=keyboard)
        else:
            if result.result_text:
                await call.message.answer(text=result.result_text, reply_markup=keyboard)

        if result.test:
            question = get_question_by_id(result.test)
            if question:
                answers = get_answers_question(question_id=question.id)
                keyboard_answers = InlineKeyboardMarkup()
                for answer in answers:
                    keyboard_answers.row(InlineKeyboardButton(answer.text, callback_data=answer_test_dt.new(
                        id=answer.id
                    )))
                await call.message.answer(text=question.text, reply_markup=keyboard_answers)

    else:
        await call.answer(text='Спасибо за ответ', show_alert=True)
