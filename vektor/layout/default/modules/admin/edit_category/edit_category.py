from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from keyboard.inline.edit_category import edit_category_data, get_edit_category
from keyboard.inline.get_category import get_category
from loader import dp
from modules.DataBase import get_category_by_id, edit_name_category
from states.edit_category import EditCategory


@dp.callback_query_handler(edit_category_data.filter(prefix='back'))
async def process_back_to_get_keyboard(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    keyboard = await get_category()
    await call.message.edit_text('Выберете категорию', reply_markup=keyboard)


@dp.callback_query_handler(edit_category_data.filter(prefix='category'))
async def process_edit_category(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=1)
    category_id = callback_data.get('cat_id')
    await EditCategory.name.set()
    await state.update_data(data={
        'category': category_id
    })
    await call.message.answer('Введите новое название или нажмите /cancel для отмены')


@dp.message_handler(Command('cancel'), state=EditCategory.name)
async def process_cancel_edit_category(message: types.Message, state: FSMContext):
    data = await state.get_data()
    category = get_category_by_id(int(data['category']))
    keyboard = await get_edit_category(category.id)
    await message.answer(f'Категория: {category.category}', reply_markup=keyboard)
    await state.finish()


@dp.message_handler(state=EditCategory.name)
async def process_get_new_name_category(message: types.Message, state: FSMContext):
    new_name = message.text
    data = await state.get_data()
    category = edit_name_category(category_id=data['category'], new_name=new_name)
    await state.finish()
    keyboard = await get_edit_category(category.id)
    await message.answer(f'Категория: {category.category}', reply_markup=keyboard)
