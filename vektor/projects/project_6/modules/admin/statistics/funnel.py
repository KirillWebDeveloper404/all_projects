from datetime import datetime

from aiogram import types

from keyboard.inline.statistics.funnel_statistics import generate_calendar_kb, control_months_data, day_on_month_data, \
    calendar_info_data
from keyboard.inline.statistics.start import statistics_main_data, statistics_main

from modules.Credentials import UTC_TIME_ZONE
from loader import dp
from modules.DataBase import get_statistics_funnel


@dp.callback_query_handler(statistics_main_data.filter(prefix='funnel'))
async def process_get_general_statistics(call: types.CallbackQuery):
    calendar = generate_calendar_kb()
    await call.message.edit_text("Выберете дату статистики:", reply_markup=calendar)


@dp.callback_query_handler(text='statistics_funnel_back')
async def process_back_general_statistics(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text("Статистика", reply_markup=statistics_main)


@dp.callback_query_handler(control_months_data.filter(prefix="next"), state='*')
async def process_get_next_month(call: types.CallbackQuery, callback_data: dict):
    month = int(callback_data.get("month")) + 1
    year = int(callback_data.get("year"))
    if month > 12:
        month = 1
        year += 1

    calendar = generate_calendar_kb(year, month)
    await call.message.edit_reply_markup(reply_markup=calendar)


@dp.callback_query_handler(control_months_data.filter(prefix="prev"), state='*')
async def process_get_next_month(call: types.CallbackQuery, callback_data: dict):
    await call.answer(cache_time=0)
    month = int(callback_data.get("month")) - 1
    year = int(callback_data.get("year"))
    if month < 1:
        month = 12
        year -= 1

    calendar = generate_calendar_kb(year, month)
    await call.message.edit_reply_markup(reply_markup=calendar)


# day_on_month_data
@dp.callback_query_handler(day_on_month_data.filter(), state='*')
async def process_get_next_month(call: types.CallbackQuery, callback_data: dict):
    day_on_month = callback_data.get("text")
    await call.answer(cache_time=1, text=f"Это день недели: {day_on_month}")


@dp.callback_query_handler(calendar_info_data.filter(prefix="month"))
async def process_get_next_month(call: types.CallbackQuery, callback_data: dict):
    month = int(callback_data.get("month"))
    year = int(callback_data.get("year"))
    date_calendar = datetime(year=int(year), month=int(month), day=1, tzinfo=UTC_TIME_ZONE)
    now = datetime.now(UTC_TIME_ZONE)
    if date_calendar > now:
        await call.answer(text="Этот месяц еще не наступил!")
        return

    statistic = get_statistics_funnel(month=int(month), year=int(year))
    calendar = generate_calendar_kb(year=year, month=month)
    await call.message.edit_text(statistic, reply_markup=calendar)


@dp.callback_query_handler(calendar_info_data.filter(prefix="day", day="null"))
async def process_get_next_month(call: types.CallbackQuery, callback_data: dict):
    await call.answer(cache_time=1, text=f"Такого дня нет")


@dp.callback_query_handler(calendar_info_data.filter(prefix="day"))
async def process_get_next_month(call: types.CallbackQuery, callback_data: dict):
    month = callback_data.get("month")
    year = callback_data.get("year")
    day = callback_data.get("day")
    now = datetime.now(UTC_TIME_ZONE)
    date_calendar = datetime(year=int(year), month=int(month), day=int(day), tzinfo=UTC_TIME_ZONE)
    if date_calendar > now:
        await call.answer(text="Этот день еще не наступил!")
        return
    text = f""
    statistic = get_statistics_funnel(day=int(day), month=int(month), year=int(year))
    text += statistic
    calendar = generate_calendar_kb(year=year, month=month)
    await call.message.edit_text(text, reply_markup=calendar)
