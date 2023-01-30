from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp
from modules.BotKeyboards import admin_dt, mailing_keyboard, mailing_kb_dt, admin_main, \
    admin_mailing_data, get_admin_mailing
from modules.Mailing import MailingStates
from states import DateMailing
from states.every_mailing import EveryMailing


@dp.callback_query_handler(admin_mailing_data.filter(prefix='back'), state='*')
async def process_back_to_mailing(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.answer()
    await call.message.edit_text('Рассылка', reply_markup=mailing_keyboard)


@dp.callback_query_handler(admin_dt.filter(prefix="mailing"))
async def process_start_mailing(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text(text='Выберете метод рассылки', reply_markup=mailing_keyboard)


@dp.callback_query_handler(mailing_kb_dt.filter(prefix='now_send'))
async def process_start_now_send(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    keyboard = await get_admin_mailing()
    await call.message.edit_text(text='Мгновенная рассылка', reply_markup=keyboard)
    await MailingStates.init.set()


@dp.callback_query_handler(mailing_kb_dt.filter(prefix='back'))
async def process_start_now_send(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text(text='Управление', reply_markup=admin_main)


@dp.callback_query_handler(mailing_kb_dt.filter(prefix='date_send'))
async def process_start_now_send(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    keyboard = await get_admin_mailing()
    await call.message.edit_text(text='Рассылка по дате', reply_markup=keyboard)
    await DateMailing.init.set()
    await state.update_data({
        'data': None,
        'year': None,
        'month': None,
        'day': None,
        'hour': None,
        'minute': None,
        'link': None,
        'text_link': None,
        'photo': None,
        'animation': None,
        'document': None,
        'message_text': None
    })


@dp.callback_query_handler(mailing_kb_dt.filter(prefix='every_send'))
async def process_every_send_mailing(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    keyboard = await get_admin_mailing()
    await call.message.edit_text(text='Повторяющаяся рассылка', reply_markup=keyboard)
    await EveryMailing.init.set()
    await state.update_data({
        'data': None,
        'every_day': None,
        'every_day_of_week': None,
        'every_month': None,
        'day_of_week': None,
        'day_of_month': None,
        'hour': None,
        'minute': None,
        'link': None,
        'text_link': None,
        'photo': None,
        'animation': None,
        'document': None,
        'message_text': None
    })
