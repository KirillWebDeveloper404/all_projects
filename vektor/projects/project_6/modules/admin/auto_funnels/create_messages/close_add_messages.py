from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline import generate_auto_funnels_manage
from keyboard.inline.create_message_af.all_data import close_add_message_funnel
from loader import dp, bot
from modules.DataBase import get_auto_funnel_by_id
from states import CreateMessageAF
from .save_message import save_message


@dp.callback_query_handler(close_add_message_funnel.filter(), state=CreateMessageAF.choice)
async def process_add_message_starting(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    data = await state.get_data()
    funnel_id = await save_message(data)
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
    await call.message.answer(text, reply_markup=keyboard)
    await state.finish()