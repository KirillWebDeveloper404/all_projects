from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from modules.calendar_kb import generate_calendar_kb
from states import DateMailing


@dp.callback_query_handler(state=DateMailing.init)
async def get_data_mailing(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    print(type(call.data))
    await state.update_data({'data': call.data})
    keyboard = generate_calendar_kb(back='mailing')
    await call.message.edit_text('Выберете дату рассылки', reply_markup=keyboard)
    await DateMailing.get_date.set()


