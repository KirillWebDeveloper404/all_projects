from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from modules.BotKeyboards import get_admin_mailing
from modules.Credentials import UTC_TIME_ZONE
from modules.calendar_kb import calendar_info_data, get_month_text
from states import DateMailing


@dp.callback_query_handler(calendar_info_data.filter(prefix="month"), state=DateMailing.get_date)
async def process_get_next_month(call: types.CallbackQuery, callback_data: dict):
    month = int(callback_data.get("month"))
    year = int(callback_data.get("year"))
    await call.answer(text=f'Месяц: {get_month_text(month)} {year}')


@dp.callback_query_handler(calendar_info_data.filter(prefix="day", day="null"), state=DateMailing.get_date)
async def process_get_next_month(call: types.CallbackQuery):
    await call.answer(cache_time=1, text=f"Такого дня нет")


@dp.callback_query_handler(calendar_info_data.filter(prefix="day"), state=DateMailing.get_date)
async def process_get_next_month(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    month = int(callback_data.get("month"))
    year = int(callback_data.get("year"))
    day = int(callback_data.get("day"))
    now = datetime.now(tz=UTC_TIME_ZONE)
    date_calendar = datetime(year=int(year), month=int(month), day=int(day), hour=23, minute=59, second=59,
                             tzinfo=UTC_TIME_ZONE)
    if date_calendar < now:
        await call.answer(text="Этот день уже был!")
        return
    await state.update_data({'year': year, 'month': month, 'day': day})
    await call.message.edit_text('Напишите время рассылки в формате(час:минута):\n'
                                 'Примеры: 08:00, 8:05, 20:10, 20:05')
    await DateMailing.get_time.set()


@dp.callback_query_handler(text='mailing_back', state=DateMailing.get_date)
async def process_get_next_month(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await DateMailing.init.set()
    keyboard = await get_admin_mailing()
    await call.message.edit_text(text='Рассылка по дате', reply_markup=keyboard)
