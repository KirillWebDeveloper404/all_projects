from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from modules.BotKeyboards import every_mailing_dt, every_mailing_week, every_mailing_week_dt
from states.every_mailing import EveryMailing


@dp.callback_query_handler(every_mailing_dt.filter(prefix='day'), state=EveryMailing.get_type)
async def process_get_type_every_mailing(call: types.CallbackQuery, state: FSMContext):
    await state.update_data({'every_day': True})
    await call.answer(cache_time=1)
    await call.message.edit_text('Напишите время рассылки в формате(час:минута) без нулей:\n'
                                 'Примеры: 8:25, 8:5, 20:10, 20:5')
    await EveryMailing.get_time.set()


@dp.callback_query_handler(every_mailing_dt.filter(prefix='month'), state=EveryMailing.get_type)
async def process_get_type_every_mailing(call: types.CallbackQuery, state: FSMContext):
    await state.update_data({'every_month': True})
    await call.answer(cache_time=1)
    await call.message.edit_text('Напишите число месяца:')
    await EveryMailing.get_day_of_month.set()


@dp.message_handler(state=EveryMailing.get_day_of_month)
async def process_get_type_every_mailing(message: types.Message, state: FSMContext):
    day_of_month = int(message.text)
    await state.update_data({'day_of_month': day_of_month})
    await message.answer('Напишите время рассылки в формате(час:минута) без нулей:\n'
                         'Примеры: 8:25, 8:5, 20:10, 20:5')
    await EveryMailing.get_time.set()


@dp.callback_query_handler(every_mailing_dt.filter(prefix='week'), state=EveryMailing.get_type)
async def process_get_type_every_mailing(call: types.CallbackQuery, state: FSMContext):
    await state.update_data({'every_day_of_week': True})
    await call.answer(cache_time=1)
    await call.message.edit_text('Выберете день недели:', reply_markup=every_mailing_week)
    await EveryMailing.get_day_of_week.set()


@dp.callback_query_handler(every_mailing_week_dt.filter(), state=EveryMailing.get_day_of_week)
async def process_get_type_every_mailing(call: types.CallbackQuery, state: FSMContext, callback_data=dict):
    day_of_week = int(callback_data.get('prefix'))
    await state.update_data({'day_of_week': day_of_week})
    await call.answer(cache_time=1)
    await call.message.edit_text('Напишите время рассылки в формате(час:минута) без нулей:\n'
                                 'Примеры: 8:25, 8:5, 20:10, 20:5')
    await EveryMailing.get_time.set()
