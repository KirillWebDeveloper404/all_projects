from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from modules.BotKeyboards import date_send_kb_dt, mailing_keyboard
from modules.admin.mailing.functions import adding_job_every
from states.every_mailing import EveryMailing


@dp.callback_query_handler(date_send_kb_dt.filter(prefix='ok'), state=EveryMailing.final)
async def process_accept_letter(call: types.CallbackQuery, state=FSMContext):
    await call.answer(cache_time=1)
    await call.message.edit_reply_markup()
    await call.message.answer('Рассылка создана', reply_markup=mailing_keyboard)
    data = await state.get_data()
    await adding_job_every(data)
    await state.finish()


@dp.callback_query_handler(date_send_kb_dt.filter(prefix='no'), state=EveryMailing.final)
async def process_accept_letter(call: types.CallbackQuery, state=FSMContext):
    await call.answer(cache_time=1)
    await call.message.edit_reply_markup()
    await call.message.answer('Рассылка отменена', reply_markup=mailing_keyboard)
    await state.finish()