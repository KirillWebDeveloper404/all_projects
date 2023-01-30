from aiogram import types

from keyboard.inline import auto_funnels_list_data, generate_auto_funnels_manage, auto_funnels_manage_data, \
    generate_list_auto_funnels
from loader import dp, bot
from modules.DataBase import get_auto_funnel_by_id


@dp.callback_query_handler(auto_funnels_list_data.filter(prefix='auto_funnels'))
async def get_auto_funnel_info(call: types.CallbackQuery, callback_data: dict):
    auto_funnel_id = int(callback_data.get('id'))
    auto_funnel = get_auto_funnel_by_id(auto_funnel_id)
    bot_info = await bot.get_me()
    text = 'Автоворонка \n' \
           f'Имя: {auto_funnel.name}\n' \
           f'Ссылка на воронку:\nhttps://t.me/{bot_info.username}?start={auto_funnel.name}\n'
    if auto_funnel.start_on_week:
        text += f'Начало в {auto_funnel.start_on_week} день недели\n\n'
    elif auto_funnel.start_on_day_month:
        text += f'Начало в {auto_funnel.start_on_day_month}-ый день месяца\n\n'
    elif auto_funnel.fast_start:
        text += f'Начало: мгновенно\n\n'

    if auto_funnel.product_id:
        text += f'Продукт: {auto_funnel.product_id.name}\n'

    if auto_funnel.job_buy:
        if auto_funnel.job_buy == 'stop':
            text += 'После покупки будет остоновлена\n'
        else:
            funnel_redirect = get_auto_funnel_by_id(int(auto_funnel.job_buy))
            text += f'После покупки: редирект на {funnel_redirect.name}\n'

    if auto_funnel.job_not_buy:
        funnel_redirect = get_auto_funnel_by_id(int(auto_funnel.job_not_buy))
        text += f'После покупки: редирект на {funnel_redirect.name}\n'

    text += f'Воронка создана {auto_funnel.created_ts}\n'

    keyboard = await generate_auto_funnels_manage(auto_funnel.id)
    await call.answer(cache_time=1)
    await call.message.edit_text(text, reply_markup=keyboard)


@dp.callback_query_handler(auto_funnels_manage_data.filter(prefix='back'))
async def process_back_to_list(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    keyboard = await generate_list_auto_funnels()
    await call.message.edit_text('Автоворонки', reply_markup=keyboard)
