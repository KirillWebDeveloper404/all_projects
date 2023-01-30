from aiogram import types

from keyboard.inline import auto_funnels_manage_data, generate_accept_delete_funnels, accept_delete_funnels_data, \
    generate_list_auto_funnels, generate_auto_funnels_manage
from loader import dp
from modules.DataBase import delete_auto_funnel_by_id, get_auto_funnel_by_id


@dp.callback_query_handler(auto_funnels_manage_data.filter(prefix='delete'))
async def process_send_accept_delete_funnels(call: types.CallbackQuery, callback_data: dict):
    funnel_id = int(callback_data.get('id'))
    await call.answer(cache_time=1)
    keyboard = await generate_accept_delete_funnels(funnel_id)
    await call.message.edit_text('Вы уверены что хотите удалить эту воронку', reply_markup=keyboard)


@dp.callback_query_handler(accept_delete_funnels_data.filter(prefix='accept'))
async def process_delete_funnels(call: types.CallbackQuery, callback_data: dict):
    funnel_id = int(callback_data.get('id'))
    delete_auto_funnel_by_id(funnel_id)
    await call.answer('Автоворонка успешно удалена')
    keyboard = await generate_list_auto_funnels()
    await call.message.edit_text('Автоворонки', reply_markup=keyboard)


@dp.callback_query_handler(accept_delete_funnels_data.filter(prefix='no'))
async def process_no_delete_funnel(call: types.CallbackQuery, callback_data: dict):
    auto_funnel_id = int(callback_data.get('id'))
    auto_funnel = get_auto_funnel_by_id(auto_funnel_id)
    text = 'Автоворонка \n' \
           f'Имя: {auto_funnel.name}\n'
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
