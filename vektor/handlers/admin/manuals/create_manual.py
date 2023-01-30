from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.admin.manuals.get_manual_info import send_manual_info_created, get_manuals_info, \
    get_manuals_info_by_view_admin
from keyboards.inline.admin.category_manuals import generate_category_manuals_kb
from keyboards.inline.admin.category_manuals_manage import category_manuals_manage_data
from keyboards.inline.admin.create_manual import create_manual_dt
from keyboards.inline.admin.view_manual import view_manual_admin_dt, generate_manual_view_admin_kb
from loader import dp
from states import CreateManual
from utils.db_api.manuals_model import create_manual, change_manual_by_id


@dp.callback_query_handler(category_manuals_manage_data.filter(pr='new'))
async def process_create(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    category_id = int(callback_data.get('cat_id'))
    await call.answer(cache_time=1)
    await state.update_data(data={
        'category': category_id,
        'name': None,
        'desc': None,
        'edit': False
    })
    await CreateManual.process.set()
    data = await state.get_data()
    await send_manual_info_created(data, call.message, True)


@dp.callback_query_handler(view_manual_admin_dt.filter(pr='name'))
@dp.callback_query_handler(create_manual_dt.filter(pr='name'), state=CreateManual.process)
async def process_add_name(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    try:
        manual_id = int(callback_data.get('ml_id'))
        await state.update_data(data={
            'edit': True,
            'manual_id': manual_id
        })
    except Exception as e:
        pass

    await call.answer(cache_time=1)
    await call.message.answer('Отправьте название руководства')
    await CreateManual.name.set()


@dp.message_handler(state=CreateManual.name)
async def process_get_name(message: types.Message, state: FSMContext):
    await state.update_data(data={
        'name': message.text
    })
    data = await state.get_data()
    if data['edit']:
        await state.finish()
        manual = await change_manual_by_id(manual_id=data['manual_id'], name=data['name'])
        text = await get_manuals_info_by_view_admin(manual_id=manual.id)
        keyboard = await generate_manual_view_admin_kb(category_id=manual.category, manual_id=manual.id)
        await message.answer(text, reply_markup=keyboard)
        return

    await send_manual_info_created(data, message)


@dp.callback_query_handler(view_manual_admin_dt.filter(pr='desc'))
@dp.callback_query_handler(create_manual_dt.filter(pr='desc'), state=CreateManual.process)
async def process_add_desc(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await call.answer(cache_time=1)
    try:
        manual_id = int(callback_data.get('ml_id'))
        await state.update_data(data={
            'edit': True,
            'manual_id': manual_id
        })
    except Exception as e:
        pass
    await call.message.answer('Отправьте описание руководства')
    await CreateManual.desc.set()


@dp.message_handler(state=CreateManual.desc)
async def process_get_desc(message: types.Message, state: FSMContext):
    await state.update_data(data={
        'desc': message.text
    })
    data = await state.get_data()
    if data['edit']:
        await state.finish()
        manual = await change_manual_by_id(manual_id=data['manual_id'], desc=data['desc'])
        text = await get_manuals_info_by_view_admin(manual_id=manual.id)
        keyboard = await generate_manual_view_admin_kb(category_id=manual.category, manual_id=manual.id)
        await message.answer(text, reply_markup=keyboard)
        return

    await send_manual_info_created(data, message)


@dp.callback_query_handler(create_manual_dt.filter(pr='cancel'), state=CreateManual.process)
async def process_cancel(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.answer(cache_time=1)
    keyboard = await generate_category_manuals_kb()
    await call.message.edit_text('Категории', reply_markup=keyboard)


@dp.callback_query_handler(create_manual_dt.filter(pr='save'), state=CreateManual.process)
async def process_save(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.finish()
    await call.answer(cache_time=1)
    manual = await create_manual(
        category_id=data['category'],
        name=data['name'],
        desc=data['desc']
    )
    text = await get_manuals_info_by_view_admin(manual_id=manual.id)
    keyboard = await generate_manual_view_admin_kb(category_id=manual.category, manual_id=manual.id)
    await call.message.edit_text(text, reply_markup=keyboard)
