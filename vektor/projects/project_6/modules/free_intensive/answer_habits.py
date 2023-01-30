from aiogram import types

from  loader import bot, dp
from modules.BotKeyboards import free_intensive_data, free_intensive_habits_2
from modules.DataBase import (
    get_animation_by_name,
    get_animation_by_name_tg_id,
    get_audio_by_name,
    get_photo_by_name_tg_id,
)


@dp.callback_query_handler(free_intensive_data.filter(filter="habits"))
async def process_answer_habits(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    gif = get_animation_by_name_tg_id("только честно")
    text = (
        "А теперь представьте.\n\n"
        "Вот скажу я вам завтра: всё, перестаём есть сладкое и вредное. Нельзя 🚫.\n"
        "Получится у вас долго так продержаться? Будет хотеться съесть сладости и мучное или нет?\n"
        "Пробовали ли вы уже так, и насколько эффективно просто себе запретить?👇👇👇\n\n"
        "1. «нет, я срываюсь и набираю потом вес ещё больше» \n"
        "2. «не могу долго себе запрещать – срываюсь и потом чувство вины гложет» \n"
        "3. «я держусь, долго могу себя контролировать» \n"
    )
    await bot.send_animation(
        chat_id=call.from_user.id, caption=text, animation=gif, reply_markup=free_intensive_habits_2
    )


@dp.callback_query_handler(free_intensive_data.filter(filter="habits_2"))
async def process_answer_habits(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    audio = get_audio_by_name("сила воли")
    text = (
        "Хотите вдохновляющую историю про маму 2х детей, которая раньше ела пакетами "
        "конфеты, а на курсе «как по волшебству» перестала. В чём секрет – в осознанном "
        "питании. И, конечно, в наполняющих йога-практиках. Аня пришла ко мне год « Назад. После "
        "2х КС. Знаете, она не верила, что получится. Но я верила, я знала-и получилось:+1:\n"
        "Хотите так же?"
    )
    await bot.send_audio(chat_id=call.from_user.id, caption=text, audio=audio, reply_markup=None)
    photo = get_photo_by_name_tg_id("аня")
    text = 'Кстати, с «фартуком» после КС, как у Ани, важно работать особенно бережно. Многим девушкам неприятно даже ' \
           'прикасаться к шовчику... И это понятно: ведь там спаечки... Но приверной технике всё получается исправить' \
           ' 👌 '
    await call.message.answer_photo(photo=photo, caption=text)
