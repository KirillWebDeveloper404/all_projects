from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline import create_af_data, create_auto_funnel_keyboard, get_job_buy_do, job_af_data, get_redirect, \
    redirect_af_data
from loader import dp
from modules.DataBase import get_all_auto_funnels
from states import CreateAutoFunnels
from .final_message import get_final_message


@dp.callback_query_handler(create_af_data.filter(prefix='buy'), state=CreateAutoFunnels.choice)
async def process_send_get_product(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    keyboard = await get_job_buy_do(True)
    await call.message.edit_text('Выберете действие:', reply_markup=keyboard)
    await CreateAutoFunnels.get_do_buy.set()


@dp.callback_query_handler(job_af_data.filter(prefix='stop'), state=CreateAutoFunnels.get_do_buy)
async def process_get_job_buy_stop(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await state.update_data(data={
        'if_buy': 'stop'
    })
    data = await state.get_data()
    if data['created']:
        text = await get_final_message(data)
        keyboard = await create_auto_funnel_keyboard(data)
        await call.message.edit_text(text, reply_markup=keyboard)
        await CreateAutoFunnels.choice.set()
    else:
        keyboard = await get_job_buy_do(False, data)
        await call.message.edit_text('Выберете действие если человек НЕ купил товар в воронке', reply_markup=keyboard)
        await CreateAutoFunnels.get_do_not_buy.set()



@dp.callback_query_handler(job_af_data.filter(prefix='skip_buy'), state=CreateAutoFunnels.get_do_buy)
async def process_get_job_buy_stop(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await call.answer(cache_time=1)
    keyboard = await get_job_buy_do(False, data)
    await call.message.edit_text('Выберете действие если человек НЕ купил товар в воронке', reply_markup=keyboard)
    await CreateAutoFunnels.get_do_not_buy.set()


@dp.callback_query_handler(job_af_data.filter(prefix='redirect'), state=CreateAutoFunnels.get_do_buy)
async def process_get_job_buy_stop(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    if len(get_all_auto_funnels()) < 1:
        keyboard = await get_job_buy_do(True)
        await call.message.edit_text('У вас нет воронок\nВыберете действие:', reply_markup=keyboard)
        await CreateAutoFunnels.get_do_buy.set()
        return
    keyboard = await get_redirect()
    await call.message.edit_text('Выберите воронку', reply_markup=keyboard)


@dp.callback_query_handler(redirect_af_data.filter(), state=CreateAutoFunnels.get_do_buy)
async def process_get_redirect_funnel(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    funnel_id = callback_data.get('id')
    await call.answer(cache_time=1)
    await state.update_data(data={
        'if_buy': funnel_id
    })
    data = await state.get_data()
    if data['created']:
        text = await get_final_message(data)
        keyboard = await create_auto_funnel_keyboard(data)
        await call.message.edit_text(text, reply_markup=keyboard)
        await CreateAutoFunnels.choice.set()
    else:
        keyboard = await get_job_buy_do(False, data)
        await call.message.edit_text('Выберете действие если человек НЕ купил товар в воронке', reply_markup=keyboard)
        await CreateAutoFunnels.get_do_not_buy.set()

