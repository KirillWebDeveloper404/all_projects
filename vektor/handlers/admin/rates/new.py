from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.admin.create_rate import create_rate_data
from keyboards.inline.admin.item_rate import item_rate_data
from states.create_rate import CreateRate
from utils.db_api.rates_model import create_rate, change_rate_info
from .get_info import send_info_by_create_rate, send_item_rate
from keyboards.inline.admin.rates_main import rates_main_data, rates_main
from loader import dp, bots_manager


@dp.callback_query_handler(rates_main_data.filter(pr='new'))
async def process_back(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await state.update_data(data={
        'name': None,
        'path': 'layout/default',
        'desc': None,
        'price': None,
        'edit': False,
        'rate_id': None,
    })
    data = await state.get_data()
    await send_info_by_create_rate(data=data, message=call.message, is_delete=True)


@dp.callback_query_handler(create_rate_data.filter(pr='cancel'), state=CreateRate.process)
async def process_cancel(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await state.finish()
    # await call.message.delete()
    await call.message.edit_text('Тарифы', reply_markup=rates_main)


@dp.callback_query_handler(item_rate_data.filter(pr='name'))
@dp.callback_query_handler(create_rate_data.filter(pr='name'), state=CreateRate.process)
async def process_get_name(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=1)
    await call.message.edit_text('Отправьте название тарифа')
    await CreateRate.name.set()
    try:
        rate_id = int(callback_data.get('rate_id'))
        await state.update_data(data={
            'edit': True,
            'rate_id': rate_id
        })
    except Exception:
        pass


@dp.message_handler(state=CreateRate.name)
async def process_add_name(message: types.Message, state: FSMContext):
    await state.update_data(data={'name': message.text})
    data = await state.get_data()
    if data['edit']:
        rate = await change_rate_info(rate_id=data['rate_id'], name=message.text)
        await state.finish()
        await send_item_rate(rate_id=rate.id, message=message)
        return
    await send_info_by_create_rate(data=data, message=message)


@dp.callback_query_handler(item_rate_data.filter(pr='desc'))
@dp.callback_query_handler(create_rate_data.filter(pr='desc'), state=CreateRate.process)
async def process_get_desc(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=1)
    await call.message.edit_text('Отправьте описание тарифа')
    await CreateRate.desc.set()
    try:
        rate_id = int(callback_data.get('rate_id'))
        await state.update_data(data={
            'edit': True,
            'rate_id': rate_id
        })
    except Exception:
        pass


@dp.message_handler(state=CreateRate.desc)
async def process_add_desc(message: types.Message, state: FSMContext):
    await state.update_data(data={'desc': message.text})
    data = await state.get_data()
    if data['edit']:
        rate = await change_rate_info(rate_id=data['rate_id'], desc=message.text)
        await state.finish()
        await send_item_rate(rate_id=rate.id, message=message)
        return
    await send_info_by_create_rate(data=data, message=message)


@dp.callback_query_handler(create_rate_data.filter(pr='path'), state=CreateRate.process)
async def process_get_path(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text('Отправьте путь к боту на сервере (pwd) тарифа')
    await CreateRate.path.set()


@dp.message_handler(state=CreateRate.path)
async def process_add_path(message: types.Message, state: FSMContext):
    await state.update_data(data={'path': message.text})
    data = await state.get_data()
    await send_info_by_create_rate(data=data, message=message)


@dp.callback_query_handler(item_rate_data.filter(pr='price'))
@dp.callback_query_handler(create_rate_data.filter(pr='price'), state=CreateRate.process)
async def process_get_price(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=1)
    await call.message.edit_text('Отправьте цену тарифа')
    await CreateRate.price.set()
    try:
        rate_id = int(callback_data.get('rate_id'))
        await state.update_data(data={
            'edit': True,
            'rate_id': rate_id
        })
    except Exception:
        pass


@dp.message_handler(state=CreateRate.price)
async def process_add_price(message: types.Message, state: FSMContext):
    try:
        price = int(message.text)
    except ValueError:
        await message.answer('Не правильно введена сумма (нужны только цифры)')
        return

    await state.update_data(data={'price': price})
    data = await state.get_data()
    if data['edit']:
        rate = await change_rate_info(rate_id=data['rate_id'], price=price)
        await state.finish()
        await send_item_rate(rate_id=rate.id, message=message)
        return
    await send_info_by_create_rate(data=data, message=message)


@dp.callback_query_handler(create_rate_data.filter(pr='save'), state=CreateRate.process)
async def process_get_price(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    data = await state.get_data()
    path_layout = await bots_manager.add_layout(path_layout=data['path'])
    rate = await create_rate(
        name=data['name'],
        desc=data['desc'],
        price=data['price'],
        path=path_layout
    )
    await state.finish()
    await send_item_rate(rate_id=rate.id, message=call.message, is_delete=True)
