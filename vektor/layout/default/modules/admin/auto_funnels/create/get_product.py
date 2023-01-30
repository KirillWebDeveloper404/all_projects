from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline import create_af_data, create_auto_funnel_keyboard, af_category_data, get_products, \
    af_product_data, af_manage_product, af_manage_product_data, get_job_buy_do
from keyboard.inline.auto_funnels import get_product_store
from loader import dp
from states import CreateAutoFunnels
from .final_message import get_final_message


@dp.callback_query_handler(create_af_data.filter(prefix='product'), state=CreateAutoFunnels.choice)
async def process_send_get_product(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)

    data = await state.get_data()
    keyboard = await af_manage_product(data)
    await call.message.edit_text('Выберете действие с продуктом', reply_markup=keyboard)
    await CreateAutoFunnels.get_product.set()


@dp.callback_query_handler(af_manage_product_data.filter(prefix='skip'), state=CreateAutoFunnels.get_product)
async def process_skip_product(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    data = await state.get_data()
    await state.update_data(data={
        'created': True
    })
    text = await get_final_message(data)
    keyboard = await create_auto_funnel_keyboard(data)
    await call.message.edit_text(text, reply_markup=keyboard)
    await CreateAutoFunnels.choice.set()


@dp.callback_query_handler(af_manage_product_data.filter(prefix='set'), state=CreateAutoFunnels.get_product)
async def process_set_product(call: types.CallbackQuery):
    keyboard = await get_product_store()
    await call.message.edit_text('Выберете категорию продукта', reply_markup=keyboard)


@dp.callback_query_handler(af_category_data.filter(), state=CreateAutoFunnels.get_product)
async def process_get_category_product(call: types.CallbackQuery, callback_data: dict):
    category_id = callback_data.get('id')
    await call.answer(cache_time=1)
    keyboard = await get_products(category_id)
    await call.message.edit_text('Выберете товар', reply_markup=keyboard)


@dp.callback_query_handler(af_product_data.filter(), state=CreateAutoFunnels.get_product)
async def process_get_product(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    product_id = int(callback_data.get('id'))
    await call.answer(cache_time=1)
    await state.update_data(data={
        'product': product_id
    })
    data = await state.get_data()
    if data['created']:
        text = await get_final_message(data)
        keyboard = await create_auto_funnel_keyboard(data)
        await call.message.edit_text(text, reply_markup=keyboard)
        await CreateAutoFunnels.choice.set()
    else:
        keyboard = await get_job_buy_do(True, data)
        await call.message.edit_text('Выберете действие если человек купил в товар в воронке', reply_markup=keyboard)
        await CreateAutoFunnels.get_do_buy.set()
