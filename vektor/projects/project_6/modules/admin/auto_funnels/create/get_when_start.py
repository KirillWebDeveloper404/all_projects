from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline import when_start_data, day_on_week, day_on_week_data, create_af_data, \
    when_start, create_auto_funnel_keyboard, af_manage_product, month_day_funnel_kb, month_day_funnel_data
from loader import dp
from states import CreateAutoFunnels
from .final_message import get_final_message


@dp.callback_query_handler(create_af_data.filter(prefix='start'), state=CreateAutoFunnels.choice)
async def process_send_get_name(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text('Выберете когда будет начинаться воронка:', reply_markup=when_start)
    await CreateAutoFunnels.get_when_start.set()


@dp.callback_query_handler(when_start_data.filter(prefix='fast'), state=CreateAutoFunnels.get_when_start)
async def process_create_auto_funnels_fast(call: types.CallbackQuery, state=FSMContext):
    """
    При выборе мгновенной отправки
    """
    await call.answer(cache_time=1)
    await call.message.delete()
    await state.update_data(data={
        'is_start_on_week': False,
        'is_start_on_day_month': False,
        'fast_start': True,
        'start_on_day_month': None,
        'start_on_week': None
    })
    data = await state.get_data()
    text = await get_final_message(data)
    keyboard = await create_auto_funnel_keyboard(data)
    await call.message.answer(text, reply_markup=keyboard)
    await CreateAutoFunnels.choice.set()


@dp.callback_query_handler(when_start_data.filter(prefix='week'), state=CreateAutoFunnels.get_when_start)
async def process_create_auto_funnels_fast(call: types.CallbackQuery, state=FSMContext):
    await call.answer(cache_time=1)
    await call.message.delete()
    await state.update_data(data={
        'is_start_on_week': True,
        'is_start_on_day_month': False,
        'fast_start': False,
        'start_on_day_month': None
    })
    text = 'Выберете начальный день недели'
    await call.message.answer(text, reply_markup=day_on_week)
    await CreateAutoFunnels.get_day_on_week.set()


@dp.callback_query_handler(day_on_week_data.filter(), state=CreateAutoFunnels.get_day_on_week)
async def process_get_day_on_week(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    day = int(callback_data.get('day'))
    await call.answer(cache_time=1)
    await state.update_data({'start_on_week': day})
    data = await state.get_data()
    text = await get_final_message(data)
    keyboard = await create_auto_funnel_keyboard(data)
    await call.message.edit_text(text, reply_markup=keyboard)
    await CreateAutoFunnels.choice.set()


@dp.callback_query_handler(when_start_data.filter(prefix='month'), state=CreateAutoFunnels.get_when_start)
async def process_create_auto_funnels_fast(call: types.CallbackQuery, state=FSMContext):
    await call.answer(cache_time=1)
    await call.message.delete()
    await state.update_data(data={
        'is_start_on_week': False,
        'is_start_on_day_month': True,
        'fast_start': False,
        'start_on_week': None
    })
    text = 'Выберете день месяца с которого будет начинаться воронка'
    await call.message.answer(text, reply_markup=month_day_funnel_kb)
    await CreateAutoFunnels.get_day_on_month.set()


@dp.callback_query_handler(month_day_funnel_data.filter(), state=CreateAutoFunnels.get_day_on_month)
async def get_day_on_month(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    day = int(callback_data.get('day'))
    await state.update_data(data={'start_on_day_month': day})
    data = await state.get_data()
    text = await get_final_message(data)
    keyboard = await create_auto_funnel_keyboard(data)
    await call.message.edit_text(text, reply_markup=keyboard)
    await CreateAutoFunnels.choice.set()
