from aiogram import types

from keyboard.inline import auto_funnels_manage_data, manage_messages, auto_funnels_manage_messages_data, \
    generate_auto_funnels_manage
from loader import dp, bot

from modules.DataBase import get_auto_funnel_by_id





@dp.callback_query_handler(auto_funnels_manage_messages_data.filter(prefix='back'))
async def process_back_to_edit_auto_funnel(call: types.CallbackQuery, callback_data: dict):
    funnel_id = int(callback_data.get('id'))
    auto_funnel = get_auto_funnel_by_id(funnel_id)
    bot_info = await bot.get_me()
    text = 'Автоворонка \n' \
           f'Имя: {auto_funnel.name}\n' \
           f'Ссылка на воронку:\nhttps://t.me/{bot_info.username}?start={auto_funnel.name}\n'
    if auto_funnel.start_on_week:
        text += f'Начало в {auto_funnel.start_on_week} день недели\n\n'
    elif auto_funnel.start_on_day_month:
        text += f'Начало в {auto_funnel.start_on_day_month}-ый день месяца\n\n'
    elif auto_funnel.fast_start:
        text += f'Начало на следующий день\n\n'

    text += f'Воронка создана {auto_funnel.created_ts}'

    keyboard = await generate_auto_funnels_manage(auto_funnel.id)
    await call.answer(cache_time=1)
    await call.message.edit_text(text, reply_markup=keyboard)
