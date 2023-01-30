import asyncio
import datetime
import logging

from aiogram.types import ParseMode
from aiogram.utils.exceptions import BotBlocked, ChatNotFound, UserDeactivated

from modules.Credentials import UTC_TIME_ZONE
from loader import scheduler
from  loader import bot
from modules.BotKeyboards import buy_course, intensive_invite, buy_course_2
from modules.DataBase import (
    get_animation_by_name,
    get_animation_by_name_tg_id,
    get_audio_by_name,
    get_photo_by_name,
    get_photo_by_name_tg_id,
    get_user_by_id,
    get_users_do_not_starting_intensive,
    get_users_for_free_intensive,
    get_users_for_free_intensive_where_day,
    update_user_day_for_free, get_users_friday_vebinar, get_users_friday_vebinar_all,
    change_sended_users_friday_vebinar, is_buy_korset, get_users_fre_intensive_not_buying_korset,
)
from modules.free_intensive.get_markup import get_markup, get_markup_vebinar


# Функция для предупреждения о окончании скидки
async def delete_message(message_id, chat_id):
    await bot.delete_message(chat_id=chat_id, message_id=message_id)


async def sending_end_sale(chat_id, text, keyboard, delete=False, gif=None, photo=None, delete_time=1):
    if photo:
        photo = get_photo_by_name_tg_id(photo)
    if gif:
        gif = get_animation_by_name_tg_id(gif)
    if photo:
        try:
            message_photo = await bot.send_photo(chat_id, photo=photo, parse_mode=ParseMode.MARKDOWN)
            if delete:
                delete_date = datetime.datetime.now(UTC_TIME_ZONE) + datetime.timedelta(hours=delete_time)
                scheduler.add_job(delete_message, 'date', run_date=delete_date, args=(message_photo.message_id, chat_id,))
        except (ChatNotFound, BotBlocked, UserDeactivated):
            pass
    if gif:
        try:
            message_gif = await bot.send_animation(chat_id, animation=gif, parse_mode=ParseMode.MARKDOWN)
            if delete:
                delete_date = datetime.datetime.now(UTC_TIME_ZONE) + datetime.timedelta(hours=delete_time)
                scheduler.add_job(delete_message, 'date', run_date=delete_date, args=(message_gif.message_id, chat_id,))
        except (ChatNotFound, BotBlocked, UserDeactivated):
            pass
    try:
        message = await bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)
        if delete:
            delete_date = datetime.datetime.now(UTC_TIME_ZONE) + datetime.timedelta(hours=delete_time)
            scheduler.add_job(delete_message, 'date', run_date=delete_date, args=(message.message_id, chat_id,))
    except (ChatNotFound, BotBlocked, UserDeactivated):
        pass


async def sending_lesson(day, lesson_text, photo, gif, id, audio):
    if id == 16:
        users_intensive = get_users_fre_intensive_not_buying_korset(day)
    else:
        users_intensive = get_users_for_free_intensive_where_day(day)

    markup = await get_markup(id)
    if photo:
        photo = get_photo_by_name_tg_id(photo)
    if gif:
        gif = get_animation_by_name_tg_id(gif)
    if audio:
        audio = get_audio_by_name(audio)
    if users_intensive:
        for intensive in users_intensive:
            user = get_user_by_id(intensive.user)
            if user:
                if photo:
                    try:
                        await bot.send_photo(chat_id=user.tg_id, caption=lesson_text, photo=photo, reply_markup=markup,
                                             parse_mode=ParseMode.MARKDOWN)
                        await asyncio.sleep(0.1)
                    except (ChatNotFound, BotBlocked, UserDeactivated):
                        logging.warning(f"Impossible to notify {user.tg_id}")
                    continue

                if gif:
                    try:
                        await bot.send_animation(
                            chat_id=user.tg_id, caption=lesson_text, animation=gif, reply_markup=markup,
                            parse_mode=ParseMode.MARKDOWN
                        )
                        await asyncio.sleep(0.1)
                    except (ChatNotFound, BotBlocked, UserDeactivated):
                        logging.warning(f"Impossible to notify {user.tg_id}")
                    continue

                if audio:
                    try:
                        await bot.send_audio(chat_id=user.tg_id, caption=lesson_text, audio=audio, reply_markup=markup,
                                             parse_mode=ParseMode.MARKDOWN)
                        await asyncio.sleep(0.1)
                    except (ChatNotFound, BotBlocked, UserDeactivated):
                        logging.warning(f"Impossible to notify {user.tg_id}")
                    continue

                try:
                    await bot.send_message(chat_id=user.tg_id, text=lesson_text, reply_markup=markup,
                                           parse_mode=ParseMode.MARKDOWN)
                    await asyncio.sleep(0.1)
                except (ChatNotFound, BotBlocked, UserDeactivated):
                    logging.warning(f"Impossible to notify {user.tg_id}")


async def update_users_days():
    """
    Обновляет у каждого пользователя его день подписки
    :return: -
    """
    users = get_users_for_free_intensive()
    if users:
        for user in users:
            if user:
                update_user_day_for_free(user)


async def starting_free_intensive():
    """
    Получает всех пользователей у кого день занятия равен null и присваивает им 1 день занятий
    Функция запускается только в понедельник
    :return: -
    """
    users = get_users_do_not_starting_intensive()
    for user in users:
        update_user_day_for_free(user)


# Функция входе в интенсив
async def process_buy_course(chat_id):
    await asyncio.sleep(10)
    caption_text = (
        "Ваш красивый животик ждёт вас. По результатам тестирования мы подобрали вам наилучшую "
        "программу. Это мой топовый Интенсив «Я ЖИВа». \n\n"
        "🎯 Старт занятий в понедельник\n"
        "♀Продолжительность 5 дней\n\n"
        "Что вас ждёт:\n"
        "✔ Практики для подтяжки и укрепления животика\n"
        "✔️Практики для укрепления женских мышц\n"
        "✔️Мы введём 10 минут занятий в вашу жизнь легко и с удовольствием\n"
        "✔️Скорректируем завтраки, введём главное правило питания для красивого животика\n"
        "✔️Личное сопровождение для каждой девушки.\n\n"
        "💰 Стоимость 490р вместо 990р сохраняется лишь недолго\n\n"
        "[Ссылка на YouTube](https://youtu.be/yX1DkxtruX8)"
    )

    photo = get_photo_by_name_tg_id("я жива")

    await bot.send_photo(chat_id=chat_id, photo=photo)
    await bot.send_message(chat_id=chat_id, text=caption_text, parse_mode=ParseMode.MARKDOWN, reply_markup=buy_course)
    next_run_date_1 = datetime.datetime.now(UTC_TIME_ZONE) + datetime.timedelta(hours=1)
    next_run_date_2 = datetime.datetime.now(UTC_TIME_ZONE) + datetime.timedelta(hours=3)
    next_run_date_3 = datetime.datetime.now(UTC_TIME_ZONE) + datetime.timedelta(hours=6)
    next_run_date_4 = datetime.datetime.now(UTC_TIME_ZONE) + datetime.timedelta(hours=9)
    next_run_date_6 = datetime.datetime.now(UTC_TIME_ZONE) + datetime.timedelta(hours=11)
    next_run_date_5 = datetime.datetime.now(UTC_TIME_ZONE) + datetime.timedelta(hours=24)
    text_1 = 'Специальное предложение купить Интенсив «я ЖИВа» за 490 вместо 990 действует только 12 часов!\n\n' \
             'Качать пресс не поможет. Если животик торчит-нужны особенные упражнения.\n\n' \
             'Начните заниматься 10 минут утром, поменяйте завтраки-и ваше тело преобразится.\n' \
             'Посмотрите отзыв Евгении ⬇⬇⬇\n\n' \
             'https://youtube.com/shorts/66stblv6ssM'
    text_2 = 'Бонусы-подарки  🎁  только сегодня 🔥🔥\n' \
             '🎁Техника подтяжки кожи живота\n' \
             '🎁Чек-лист «Как быстро повысить энергию и прийти в ресурсное состояние»\n' \
             '🎁Поддержка куратора в личной переписке 👌\n\n' \
             'Всё это ждёт вас бонусом к красивому животику- присоединяйтесь по ссылке ⬇️⬇️⬇️'
    text_3 = 'Красивый животик ждёт вас 👌😉 Осталось 6 часов до окончания скидки!\n' \
             '💣 Присоединяйтесь к Интенсиву по ссылке⬇️⬇️⬇️'
    text_4 = 'Какие вас ждут уроки на интенсиве:\n' \
             '✔️10-15 минут в день уроки формата «включил-повторил»\n\n' \
             'Вы научитесь правильно включать мышцы живота в работу. И уже через неделю увидите уменьшение ' \
             'сантиметров на талии. '
    text_6 = 'Через 1 час акция закончится, ссылки пропадут, такого предложения больше не будет... Очень хочу, ' \
             'чтобы вы успели и обрели красивый животик и вместе с ним уверенность в себе. '
    text_5 = 'Присоединяйся к бесплатному марафону "5 шагов к красивому животику после родов"\n\n' \
             "Стартуем в ближайший понедельник\n\n" \
             "Длительность 5 дней\n\n" \
             "Закрытое сообщество от Оксаны Роггелин, единомышленники!\n" \
             "[Ссылка на YouTube](https://www.youtube.com/watch?v=HH2KDV_52q4&feature=youtu.be)"
    scheduler.add_job(sending_end_sale, 'date',
                      run_date=next_run_date_1,
                      args=(chat_id, text_1, buy_course_2, True, None, 'спецпредложение я жива', 11))
    scheduler.add_job(sending_end_sale, 'date',
                      run_date=next_run_date_2, args=(chat_id, text_2, buy_course_2, True, None, 'бонусы я жива', 9))
    scheduler.add_job(sending_end_sale, 'date',
                      run_date=next_run_date_3, args=(chat_id, text_3, buy_course_2, True, 'красивый животик', None, 6))
    scheduler.add_job(sending_end_sale, 'date',
                      run_date=next_run_date_4, args=(chat_id, text_4, buy_course_2, True, 'успевай', None, 3))
    scheduler.add_job(sending_end_sale, 'date',
                      run_date=next_run_date_6,
                      args=(chat_id, text_6, buy_course_2, True, None, 'я жива час до конца акции', 1))
    scheduler.add_job(sending_end_sale, 'date',
                      run_date=next_run_date_5, args=(chat_id, text_5, intensive_invite))


async def sending_message_vebinar(message_text, photo, gif, audio, time_vebinar, id):
    if time_vebinar == 'all':
        users_vebinar = get_users_friday_vebinar_all()
    else:
        users_vebinar = get_users_friday_vebinar(time_vebinar)
    markup = await get_markup_vebinar(id)
    if photo:
        photo = get_photo_by_name_tg_id(photo)
    if gif:
        gif = get_animation_by_name_tg_id(gif)
    if audio:
        audio = get_audio_by_name(audio)
    if users_vebinar:
        for user_vebinar in users_vebinar:
            user = get_user_by_id(user_vebinar.user_id)
            if id == 5:
                change_sended_users_friday_vebinar(user_vebinar.id)
            if user:
                if photo:
                    try:
                        await bot.send_photo(chat_id=user.tg_id, caption=message_text, photo=photo, reply_markup=markup)
                        await asyncio.sleep(0.1)
                    except (ChatNotFound, BotBlocked, UserDeactivated):
                        logging.warning(f"Impossible to notify {user.tg_id}")
                    continue

                if gif:
                    try:
                        await bot.send_animation(
                            chat_id=user.tg_id, caption=message_text, animation=gif, reply_markup=markup
                        )
                        await asyncio.sleep(0.1)
                    except (ChatNotFound, BotBlocked, UserDeactivated):
                        logging.warning(f"Impossible to notify {user.tg_id}")
                    continue

                if audio:
                    try:
                        await bot.send_audio(chat_id=user.tg_id, caption=message_text, audio=audio, reply_markup=markup)
                        await asyncio.sleep(0.1)
                    except (ChatNotFound, BotBlocked, UserDeactivated):
                        logging.warning(f"Impossible to notify {user.tg_id}")
                    continue

                try:
                    await bot.send_message(chat_id=user.tg_id, text=message_text, reply_markup=markup)
                    await asyncio.sleep(0.1)
                except (ChatNotFound, BotBlocked, UserDeactivated):
                    logging.warning(f"Impossible to notify {user.tg_id}")
