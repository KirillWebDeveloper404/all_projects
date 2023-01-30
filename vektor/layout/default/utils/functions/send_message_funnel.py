import asyncio
import datetime
import logging
from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from aiogram.utils.exceptions import BotBlocked, ChatNotFound, UserDeactivated

from keyboard.inline.tests.call_datas import answer_test_dt
from loader import bot, scheduler
from modules.Credentials import UTC_TIME_ZONE
from modules.DataBase import get_message_af_by_id, MessageAutoFunnels, get_users_af_by_funnel_id, UserAutoFunnels, \
    get_messages_by_interval_msg, check_bought_product_by_product_id, exit_user_funnel, \
    get_first_message_af_by_funnel_id, get_last_message_af, get_user_by_tg_id, get_question_by_id, get_answers_question
from utils.functions import has_text_youtube_link
from utils.functions.delete_msg_timer import delete_msg_for_timer
from utils.functions.register_user_on_funnel import register_user_on_funnel


async def send_message_funnel(message_id):
    msg: MessageAutoFunnels = get_message_af_by_id(message_id)
    users_af: List[UserAutoFunnels] = get_users_af_by_funnel_id(msg.auto_funnel_id)
    all_interval_messages = get_messages_by_interval_msg(msg.id)

    text = msg.message_text
    photo = msg.photo
    gif = msg.gif
    video = msg.video
    voice = msg.voice
    video_note = msg.video_note
    document = msg.document
    audio = msg.audio
    link = msg.link
    text_link = msg.text_link
    last_msg = get_last_message_af(msg.auto_funnel_id)

    product = msg.auto_funnel_id.product_id
    funnel_buy = msg.auto_funnel_id.job_buy

    has_youtube_link = await has_text_youtube_link(text)

    # Создание клавиатуры с ссылкой
    if link:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text_link, url=link)
                ]
            ]
        )
    else:
        keyboard = None
    users_interval = []
    for user in users_af:
        is_buy = await ridirect_buy_product_user(product, funnel_buy, user, msg.auto_funnel_id)
        if is_buy:
            return
        if user.day == msg.day:
            try:
                if photo:
                    if has_youtube_link:
                        msg_1 = await bot.send_photo(chat_id=user.user.tg_id, photo=photo)
                        await delete_timer_add_job(msg_1, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                                   msg.delete_second, user.user.tg_id)
                        if text:
                            msg_2 = await bot.send_message(chat_id=user.user.tg_id, text=text, reply_markup=keyboard)
                            await delete_timer_add_job(msg_2, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                                       msg.delete_second, user.user.tg_id)

                    else:
                        msg_3 = await bot.send_photo(chat_id=user.user.tg_id, photo=photo, caption=text,
                                                     reply_markup=keyboard)
                        await delete_timer_add_job(msg_3, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                                   msg.delete_second, user.user.tg_id)



                elif gif:
                    if has_youtube_link:
                        msg_1 = await bot.send_animation(chat_id=user.user.tg_id, animation=gif)
                        await delete_timer_add_job(msg_1, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                                   msg.delete_second, user.user.tg_id)
                        if text:
                            msg_2 = await bot.send_message(chat_id=user.user.tg_id, text=text, reply_markup=keyboard)
                            await delete_timer_add_job(msg_2, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                                       msg.delete_second, user.user.tg_id)

                    else:
                        msg_3 = await bot.send_animation(chat_id=user.user.tg_id, animation=gif, caption=text,
                                                         reply_markup=keyboard)
                        await delete_timer_add_job(msg_3, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                                   msg.delete_second, user.user.tg_id)

                elif video:
                    if has_youtube_link:
                        msg_1 = await bot.send_video(chat_id=user.user.tg_id, video=video)
                        scheduler.add_job(delete_msg_for_timer, 'interval', (msg_1, user.user.tg_id),
                                          minutes=msg.delete_minute, seconds=msg.delete_second, hours=msg.delete_hour,
                                          days=msg.delete_day, name='delete_message_af_job')
                        if text:
                            msg_2 = await bot.send_message(chat_id=user.user.tg_id, text=text, reply_markup=keyboard)
                            await delete_timer_add_job(msg_2, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                                       msg.delete_second, user.user.tg_id)

                    else:
                        msg_3 = await bot.send_video(chat_id=user.user.tg_id, video=video, caption=text,
                                                     reply_markup=keyboard)
                        await delete_timer_add_job(msg_3, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                                   msg.delete_second, user.user.tg_id)

                elif audio:
                    if has_youtube_link:
                        msg_1 = await bot.send_audio(chat_id=user.user.tg_id, audio=audio)
                        await delete_timer_add_job(msg_1, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                                   msg.delete_second, user.user.tg_id)
                        if text:
                            msg_2 = await bot.send_message(chat_id=user.user.tg_id, text=text, reply_markup=keyboard)
                            await delete_timer_add_job(msg_2, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                                       msg.delete_second, user.user.tg_id)

                    else:
                        msg_3 = await bot.send_audio(chat_id=user.user.tg_id, audio=audio, caption=text,
                                                     reply_markup=keyboard)
                        await delete_timer_add_job(msg_3, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                                   msg.delete_second, user.user.tg_id)


                elif document:
                    if has_youtube_link:
                        msg_1 = await bot.send_document(chat_id=user.user.tg_id, document=document)
                        await delete_timer_add_job(msg_1, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                                   msg.delete_second, user.user.tg_id)
                        if text:
                            msg_2 = await bot.send_message(chat_id=user.user.tg_id, text=text, reply_markup=keyboard)
                            await delete_timer_add_job(msg_2, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                                       msg.delete_second, user.user.tg_id)

                    else:
                        msg_3 = await bot.send_document(chat_id=user.user.tg_id, document=document, caption=text,
                                                        reply_markup=keyboard)
                        await delete_timer_add_job(msg_3, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                                   msg.delete_second, user.user.tg_id)

                elif video_note:
                    msg_1 = await bot.send_video_note(chat_id=user.user.tg_id, video_note=video_note, reply_markup=keyboard)
                    await delete_timer_add_job(msg_1, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                               msg.delete_second, user.user.tg_id)

                elif voice:
                    msg_1 = await bot.send_voice(chat_id=user.user.tg_id, voice=voice, reply_markup=keyboard)
                    await delete_timer_add_job(msg_1, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                               msg.delete_second, user.user.tg_id)
                elif text:
                    msg_1 = await bot.send_message(chat_id=user.user.tg_id, text=text, reply_markup=keyboard)
                    await delete_timer_add_job(msg_1, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                               msg.delete_second, user.user.tg_id)

                if last_msg.id == msg.id:
                    exit_user_funnel(user, msg.auto_funnel_id)  # Остановка воронки

                if msg.test:
                    question = get_question_by_id(msg.test)
                    if question:
                        answers = get_answers_question(question_id=question.id)
                        keyboard_answers = InlineKeyboardMarkup()
                        for answer in answers:
                            keyboard_answers.row(InlineKeyboardButton(answer.text, callback_data=answer_test_dt.new(
                                id=answer.id
                            )))
                        await bot.send_message(chat_id=user.user.tg_id, text=question.text,
                                               reply_markup=keyboard_answers)

                users_interval.append(user.user.tg_id)
                await asyncio.sleep(0.1)
            except (BotBlocked, ChatNotFound, UserDeactivated):
                logging.warning(f"Impossible to notify {user.user.tg_id}")

            if all_interval_messages:
                for interval_message in all_interval_messages:
                    if not interval_message.interval_minute:
                        interval_minute = 0
                    else:
                        interval_minute = interval_message.interval_minute
                    if not interval_message.interval_second:
                        interval_second = 0
                    else:
                        interval_second = interval_message.interval_second
                    if not interval_message.interval_hour:
                        interval_hour = 0
                    else:
                        interval_hour = interval_message.interval_hour
                    if not interval_message.interval_day:
                        interval_day = 0
                    else:
                        interval_day = interval_message.interval_day

                    run_date = datetime.datetime.now() + datetime.timedelta(days=interval_day, hours=interval_hour,
                                                                            minutes=interval_minute,
                                                                            seconds=interval_second)

                    scheduler.add_job(send_message_funnel_for_interval, 'date', (interval_message.id, users_interval),
                                      run_date=run_date, name=f'interval_message_af_{interval_message.id}')


async def send_message_funnel_for_interval(message_id, users):
    msg: MessageAutoFunnels = get_message_af_by_id(message_id)

    text = msg.message_text
    photo = msg.photo
    gif = msg.gif
    video = msg.video
    voice = msg.voice
    video_note = msg.video_note
    document = msg.document
    audio = msg.audio
    link = msg.link
    text_link = msg.text_link

    has_youtube_link = await has_text_youtube_link(text)

    # Создание клавиатуры с ссылкой
    if link:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text_link, url=link)
                ]
            ]
        )
    else:
        keyboard = None
    for chat_id in users:
        try:
            if photo:
                if has_youtube_link:
                    msg_1 = await bot.send_photo(chat_id=chat_id, photo=photo)
                    await delete_timer_add_job(msg_1, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                               msg.delete_second, chat_id)
                    if text:
                        msg_2 = await bot.send_message(chat_id=chat_id, text=text,
                                                       reply_markup=keyboard)
                        await delete_timer_add_job(msg_2, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                                   msg.delete_second, chat_id)

                else:
                    msg_3 = await bot.send_photo(chat_id=chat_id, photo=photo, caption=text,
                                                 reply_markup=keyboard)
                    await delete_timer_add_job(msg_3, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                               msg.delete_second, chat_id)



            elif gif:
                if has_youtube_link:
                    msg_1 = await bot.send_animation(chat_id=chat_id, animation=gif)
                    await delete_timer_add_job(msg_1, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                               msg.delete_second, chat_id)
                    if text:
                        msg_2 = await bot.send_message(chat_id=chat_id, text=text,
                                                       reply_markup=keyboard)
                        await delete_timer_add_job(msg_2, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                                   msg.delete_second, chat_id)

                else:
                    msg_3 = await bot.send_animation(chat_id=chat_id, animation=gif, caption=text,
                                                     reply_markup=keyboard)
                    await delete_timer_add_job(msg_3, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                               msg.delete_second, chat_id)

            elif video:
                if has_youtube_link:
                    msg_1 = await bot.send_video(chat_id=chat_id, video=video)
                    scheduler.add_job(delete_msg_for_timer, 'interval', (msg_1, chat_id),
                                      minutes=msg.delete_minute, seconds=msg.delete_second,
                                      hours=msg.delete_hour,
                                      days=msg.delete_day, name='delete_message_af_job')
                    if text:
                        msg_2 = await bot.send_message(chat_id=chat_id, text=text,
                                                       reply_markup=keyboard)
                        await delete_timer_add_job(msg_2, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                                   msg.delete_second, chat_id)

                else:
                    msg_3 = await bot.send_video(chat_id=chat_id, video=video, caption=text,
                                                 reply_markup=keyboard)
                    await delete_timer_add_job(msg_3, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                               msg.delete_second, chat_id)

            elif audio:
                if has_youtube_link:
                    msg_1 = await bot.send_audio(chat_id=chat_id, audio=audio)
                    await delete_timer_add_job(msg_1, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                               msg.delete_second, chat_id)
                    if text:
                        msg_2 = await bot.send_message(chat_id=chat_id, text=text,
                                                       reply_markup=keyboard)
                        await delete_timer_add_job(msg_2, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                                   msg.delete_second, chat_id)

                else:
                    msg_3 = await bot.send_audio(chat_id=chat_id, audio=audio, caption=text,
                                                 reply_markup=keyboard)
                    await delete_timer_add_job(msg_3, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                               msg.delete_second, chat_id)


            elif document:
                if has_youtube_link:
                    msg_1 = await bot.send_document(chat_id=chat_id, document=document)
                    await delete_timer_add_job(msg_1, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                               msg.delete_second, chat_id)
                    if text:
                        msg_2 = await bot.send_message(chat_id=chat_id, text=text,
                                                       reply_markup=keyboard)
                        await delete_timer_add_job(msg_2, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                                   msg.delete_second, chat_id)

                else:
                    msg_3 = await bot.send_document(chat_id=chat_id, document=document, caption=text,
                                                    reply_markup=keyboard)
                    await delete_timer_add_job(msg_3, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                               msg.delete_second, chat_id)

            elif video_note:
                msg_1 = await bot.send_video_note(chat_id=chat_id, video_note=video_note, reply_markup=keyboard)
                await delete_timer_add_job(msg_1, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                           msg.delete_second, chat_id)

            elif voice:
                msg_1 = await bot.send_voice(chat_id=chat_id, voice=voice, reply_markup=keyboard)
                await delete_timer_add_job(msg_1, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                           msg.delete_second, chat_id)
            elif text:
                msg_1 = await bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)
                await delete_timer_add_job(msg_1, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                           msg.delete_second, chat_id)

            if msg.test:
                question = get_question_by_id(msg.test)
                if question:
                    answers = get_answers_question(question_id=question.id)
                    keyboard_answers = InlineKeyboardMarkup()
                    for answer in answers:
                        keyboard_answers.row(InlineKeyboardButton(answer.text, callback_data=answer_test_dt.new(
                            id=answer.id
                        )))
                    await bot.send_message(chat_id=chat_id, text=question.text, reply_markup=keyboard_answers)

            await asyncio.sleep(0.1)
        except (BotBlocked, ChatNotFound, UserDeactivated):
            logging.warning(f"Impossible to notify {chat_id}")


async def send_first_message_funnel(message_id, chat_id):
    msg: MessageAutoFunnels = get_message_af_by_id(message_id)
    all_interval_messages = get_messages_by_interval_msg(msg.id)
    print(all_interval_messages, "интервал сообщений")
    text = msg.message_text
    photo = msg.photo
    gif = msg.gif
    video = msg.video
    voice = msg.voice
    video_note = msg.video_note
    document = msg.document
    audio = msg.audio
    link = msg.link
    text_link = msg.text_link
    product = msg.auto_funnel_id.product_id
    funnel_buy = msg.auto_funnel_id.job_buy

    has_youtube_link = await has_text_youtube_link(text)
    user = get_user_by_tg_id(chat_id)
    is_buy = await ridirect_buy_product_user(product, funnel_buy, user, msg.auto_funnel_id)
    if is_buy:
        return
    # Создание клавиатуры с ссылкой
    if link:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text_link, url=link)
                ]
            ]
        )
    else:
        keyboard = None
    users_interval = []
    try:
        if photo:
            if has_youtube_link:
                msg_1 = await bot.send_photo(chat_id=chat_id, photo=photo)
                await delete_timer_add_job(msg_1, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                           msg.delete_second, chat_id)
                if text:
                    msg_2 = await bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)
                    await delete_timer_add_job(msg_2, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                               msg.delete_second, chat_id)

            else:
                msg_3 = await bot.send_photo(chat_id=chat_id, photo=photo, caption=text,
                                             reply_markup=keyboard)
                await delete_timer_add_job(msg_3, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                           msg.delete_second, chat_id)



        elif gif:
            if has_youtube_link:
                msg_1 = await bot.send_animation(chat_id=chat_id, animation=gif)
                await delete_timer_add_job(msg_1, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                           msg.delete_second, chat_id)
                if text:
                    msg_2 = await bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)
                    await delete_timer_add_job(msg_2, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                               msg.delete_second, chat_id)

            else:
                msg_3 = await bot.send_animation(chat_id=chat_id, animation=gif, caption=text,
                                                 reply_markup=keyboard)
                await delete_timer_add_job(msg_3, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                           msg.delete_second, chat_id)

        elif video:
            if has_youtube_link:
                msg_1 = await bot.send_video(chat_id=chat_id, video=video)
                await delete_timer_add_job(msg_1, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                           msg.delete_second, chat_id)
                if text:
                    msg_2 = await bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)
                    await delete_timer_add_job(msg_2, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                               msg.delete_second, chat_id)

            else:
                msg_3 = await bot.send_video(chat_id=chat_id, video=video, caption=text,
                                             reply_markup=keyboard)
                await delete_timer_add_job(msg_3, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                           msg.delete_second, chat_id)

        elif audio:
            if has_youtube_link:
                msg_1 = await bot.send_audio(chat_id=chat_id, audio=audio)
                await delete_timer_add_job(msg_1, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                           msg.delete_second, chat_id)
                if text:
                    msg_2 = await bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)
                    await delete_timer_add_job(msg_2, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                               msg.delete_second, chat_id)

            else:
                msg_3 = await bot.send_audio(chat_id=chat_id, audio=audio, caption=text,
                                             reply_markup=keyboard)
                await delete_timer_add_job(msg_3, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                           msg.delete_second, chat_id)

        elif document:
            if has_youtube_link:
                msg_1 = await bot.send_document(chat_id=chat_id, document=document)
                await delete_timer_add_job(msg_1, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                           msg.delete_second, chat_id)
                if text:
                    msg_2 = await bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)
                    await delete_timer_add_job(msg_2, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                               msg.delete_second, chat_id)

            else:
                msg_3 = await bot.send_document(chat_id=chat_id, document=document, caption=text,
                                                reply_markup=keyboard)
                await delete_timer_add_job(msg_3, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                           msg.delete_second, chat_id)

        elif video_note:
            msg_1 = await bot.send_video_note(chat_id=chat_id, video_note=video_note, reply_markup=keyboard)
            await delete_timer_add_job(msg_1, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                       msg.delete_second, chat_id)

        elif voice:
            msg_1 = await bot.send_voice(chat_id=chat_id, voice=voice, reply_markup=keyboard)
            await delete_timer_add_job(msg_1, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                       msg.delete_second, chat_id)
        elif text:
            msg_1 = await bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)
            await delete_timer_add_job(msg_1, msg.delete_hour, msg.delete_day, msg.delete_minute,
                                       msg.delete_second, chat_id)

        if msg.test:
            question = get_question_by_id(msg.test)
            if question:
                answers = get_answers_question(question_id=question.id)
                keyboard_answers = InlineKeyboardMarkup()
                for answer in answers:
                    keyboard_answers.row(InlineKeyboardButton(answer.text, callback_data=answer_test_dt.new(
                        id=answer.id
                    )))
                await bot.send_message(chat_id=chat_id, text=question.text, reply_markup=keyboard_answers)
        users_interval.append(chat_id)
    except (BotBlocked, ChatNotFound, UserDeactivated):
        logging.warning(f"Impossible to notify {chat_id}")

    if all_interval_messages:
        for interval_message in all_interval_messages:
            if not interval_message.interval_minute:
                interval_minute = 0
            else:
                interval_minute = interval_message.interval_minute
            if not interval_message.interval_second:
                interval_second = 0
            else:
                interval_second = interval_message.interval_second
            if not interval_message.interval_hour:
                interval_hour = 0
            else:
                interval_hour = interval_message.interval_hour
            if not interval_message.interval_day:
                interval_day = 0
            else:
                interval_day = interval_message.interval_day

            run_date = datetime.datetime.now(tz=UTC_TIME_ZONE) + datetime.timedelta(days=interval_day, hours=interval_hour,
                                                                    minutes=interval_minute, seconds=interval_second)

            print(run_date, "run_date")
            scheduler.add_job(send_message_funnel_for_interval, 'date', (interval_message.id, users_interval),
                              run_date=run_date, name=f'interval_message_af_{interval_message.id}')


async def ridirect_buy_product_user(product, job_buy, user, funnel):
    is_buy = check_bought_product_by_product_id(user, product)
    if is_buy:
        if job_buy:
            exit_user_funnel(user, funnel)  # Остановка воронки
            if job_buy == 'stop':
                pass
            else:
                await register_user_on_funnel(funnel_id=job_buy, chat_id=user.tg_id)  # Редирект воронки
                message_af = get_first_message_af_by_funnel_id(funnel_id=job_buy)
                await send_first_message_funnel(message_af.id, user.tg_id)
            return True
        else:
            return False
    else:
        return False


async def delete_timer_add_job(msg, delete_hour, delete_day, delete_minute, delete_second, chat_id):
    if delete_hour or delete_day or delete_minute or delete_second:
        if not delete_hour:
            delete_hour = 0
        if not delete_day:
            delete_day = 0
        if not delete_minute:
            delete_minute = 0
        if not delete_second:
            delete_second = 0

        run_date = datetime.datetime.now(tz=UTC_TIME_ZONE) + datetime.timedelta(days=delete_day, hours=delete_hour,
                                                                minutes=delete_minute,
                                                                seconds=delete_second)
        print(run_date, "run_date")
        scheduler.add_job(func=delete_msg_for_timer, trigger='date', run_date=run_date,
                          args=(msg.message_id, chat_id,), name='dsfasdfasf')
