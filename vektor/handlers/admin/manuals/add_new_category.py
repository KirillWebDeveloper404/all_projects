from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from keyboards.inline.admin.category_manuals import category_manuals_data, generate_category_manuals_kb
from keyboards.inline.admin.category_manuals_manage import generate_category_manuals_manage_kb
from loader import dp
from states.create_category_manuals import CreateCategoryManuals
from utils.db_api.categories_manuals_model import create_category_manual


@dp.callback_query_handler(category_manuals_data.filter(pr='new'))
async def process_back(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text('Введите название категории или нажмите /cancel')
    await CreateCategoryManuals.name.set()


@dp.message_handler(Command('cancel'), state=CreateCategoryManuals.all_states)
async def process_cancel_create(message: types.Message, state: FSMContext):
    await state.finish()
    keyboard = await generate_category_manuals_kb()
    await message.answer('Категории', reply_markup=keyboard)


@dp.message_handler(state=CreateCategoryManuals.name)
async def process_get(message: types.Message, state: FSMContext):
    await state.finish()
    category = await create_category_manual(message.text)
    text = f'Категория: {category.name}\n'
    keyboard = await generate_category_manuals_manage_kb(category.id)
    await message.answer(text, reply_markup=keyboard)