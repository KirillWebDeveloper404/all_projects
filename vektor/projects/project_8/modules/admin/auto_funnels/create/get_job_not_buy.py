from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline import create_af_data, create_auto_funnel_keyboard, get_job_buy_do, job_af_data, get_redirect, \
    redirect_af_data
from loader import dp
from modules.DataBase import get_all_auto_funnels
from states import CreateAutoFunnels
from .final_message import get_final_message


@dp.callback_query_handler(create_af_data.filter(prefix='not_buy'), state=CreateAutoFunnels.choice)
async def process_send_get_product(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    if len(get_all_auto_funnels()) < 1:
        data = await state.get_data()
        keyboard = await create_auto_funnel_keyboard(data)
        text = await get_final_message(data)
        await call.message.edit_text(f'У вас нет других воронок\n\n{text}', reply_markup=keyboard)
        await CreateAutoFunnels.choice.set()
        return
    keyboard = await get_job_buy_do(False)
    await call.message.edit_text('Выберете действие:', reply_markup=keyboard)
    await CreateAutoFunnels.get_do_not_buy.set()


@dp.callback_query_handler(job_af_data.filter(prefix='skip_not_buy'), state=CreateAutoFunnels.get_do_not_buy)
async def process_get_job_buy_stop(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await state.update_data(data={
        'created': True
    })
    data = await state.get_data()
    text = await get_final_message(data)
    keyboard = await create_auto_funnel_keyboard(data)
    await call.message.edit_text(text, reply_markup=keyboard)
    await CreateAutoFunnels.choice.set()

@dp.callback_query_handler(job_af_data.filter(prefix='redirect_not_buy'), state=CreateAutoFunnels.get_do_not_buy)
async def process_get_job_buy_stop(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    keyboard = await get_redirect()
    await call.message.edit_text('Выберите воронку', reply_markup=keyboard)


@dp.callback_query_handler(redirect_af_data.filter(), state=CreateAutoFunnels.get_do_not_buy)
async def process_get_redirect_funnel(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    funnel_id = callback_data.get('id')
    await call.answer(cache_time=1)
    await state.update_data(data={
        'if_not_buy': funnel_id
    })
    data = await state.get_data()
    text = await get_final_message(data)
    keyboard = await create_auto_funnel_keyboard(data)
    await call.message.edit_text(text, reply_markup=keyboard)
    await CreateAutoFunnels.choice.set()
