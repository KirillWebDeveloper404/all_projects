from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from keyboards.inline.manuals.list_cat_manuals import generate_category_manuals_kb
from loader import dp


@dp.message_handler(Text(equals='📓 Руководство'), state='*')
async def process_start(message: types.Message, state: FSMContext):
    await state.finish()
    keyboard = await generate_category_manuals_kb()
    await message.answer('Выберете категорию руководства', reply_markup=keyboard)

