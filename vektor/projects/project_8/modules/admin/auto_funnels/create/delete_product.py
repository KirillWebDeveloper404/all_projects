from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline import create_auto_funnel_keyboard, af_manage_product_data
from loader import dp
from states import CreateAutoFunnels
from .final_message import get_final_message


@dp.callback_query_handler(af_manage_product_data.filter(prefix='delete'), state=CreateAutoFunnels.get_product)
async def process_skip_product(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await state.update_data(data={
        'if_buy': None,
        'if_not_buy': None,
        'product': None,
    })
    data = await state.get_data()
    text = await get_final_message(data)
    keyboard = await create_auto_funnel_keyboard(data)
    await call.message.edit_text(text, reply_markup=keyboard)
