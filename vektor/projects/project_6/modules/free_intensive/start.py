import datetime

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import ParseMode

from modules.Credentials import UTC_TIME_ZONE
from loader import scheduler
from  loader import bot, dp
from modules.BotKeyboards import buy_course, free_intensive_data, intensive_invite, buy_course_2
from modules.DataBase import get_photo_by_name_tg_id, get_user_for_free_intensive, register_user_on_free_intensive
from modules.free_intensive.function import sending_end_sale


@dp.callback_query_handler(text="pay_intensive_start")
async def process_invite_pay_intensive(call: types.CallbackQuery):
    caption_text = (
        "Ваш красивый животик ждёт вас. \n"
        "По результатам тестирования мы подобрали вам наилучшую программу. Это мой топовый Интенсив «Я ЖИВа».  \n\n"
        "🎯Старт занятий в понедельник\n"
        "♀Продолжительность 5 дней\n\n"
        "Что вас ждёт:\n"
        "✔️Практики для подтяжки и укрепления животика\n"
        "✔️Практики для укрепления женских мышц\n"
        "✔️Мы введём 10 минут занятий в вашу жизнь легко и с удовольствием\n"
        "✔️Скорректируем завтраки, введём главное правило питания для красивого животика\n"
        "✔️Личное сопровождение для каждой девушки.\n\n"
        "💵 Стоимость 490р вместо 990р сохраняется лишь недолго\n\n"
        "[Ссылка на YouTube](https://youtu.be/yX1DkxtruX8)"
    )

    photo = get_photo_by_name_tg_id("я жива")

    await bot.send_photo(
        chat_id=call.from_user.id,
        photo=photo,
    )
    await call.message.answer(caption_text, reply_markup=buy_course, parse_mode=ParseMode.MARKDOWN)
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
                      args=(call.from_user.id, text_1, buy_course_2, True, None, 'спецпредложение я жива'))
    scheduler.add_job(sending_end_sale, 'date',
                      run_date=next_run_date_2,
                      args=(call.from_user.id, text_2, buy_course_2, True, None, 'бонусы я жива'))
    scheduler.add_job(sending_end_sale, 'date',
                      run_date=next_run_date_3,
                      args=(call.from_user.id, text_3, buy_course_2, True, 'красивый животик', None))
    scheduler.add_job(sending_end_sale, 'date',
                      run_date=next_run_date_4, args=(call.from_user.id, text_4, buy_course_2, True, 'успевай', None))
    scheduler.add_job(sending_end_sale, 'date',
                      run_date=next_run_date_6,
                      args=(call.from_user.id, text_6, buy_course_2, True, None, 'я жива час до конца акции'))
    scheduler.add_job(sending_end_sale, 'date',
                      run_date=next_run_date_5, args=(call.from_user.id, text_5, intensive_invite))


@dp.callback_query_handler(text="free_intensive_start")
@dp.callback_query_handler(free_intensive_data.filter(filter="invite_link"))
async def process_invite(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.delete()
    text = (
        'Присоединяйся к бесплатному марафону "5 шагов к красивому животику после родов"\n\n'
        "Стартуем в ближайший понедельник\n\n"
        "Длительность 5 дней\n\n"
        "Закрытое сообщество от Оксаны Роггелин, единомышленники!\n"
        "[Ссылка на YouTube](https://www.youtube.com/watch?v=HH2KDV_52q4&feature=youtu.be)"
    )
    await call.message.answer(text=text, reply_markup=intensive_invite, parse_mode=ParseMode.MARKDOWN)


@dp.callback_query_handler(free_intensive_data.filter(filter="start"))
async def process_starting_intensive(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    user = get_user_for_free_intensive(call.from_user.id)
    if user:
        await call.message.edit_reply_markup()
        await call.message.edit_text(
            "Вы уже зарегистрированы на бесплатный интенсив.\n\nИнтенсив начнется в ближайший понедельник!"
        )
    else:
        await call.message.edit_reply_markup()
        await call.message.edit_text(
            "Вы успешно зарегистрированы на бесплатный интенсив.\n\nИнтенсив начнется в ближайший понедельник!"
        )
        register_user_on_free_intensive(call.from_user.id)
