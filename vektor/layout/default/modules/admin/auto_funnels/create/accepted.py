from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline import auto_funnels_menu, generate_list_auto_funnels, create_af_data
from loader import dp
from modules.DataBase import create_auto_funnels
from modules.admin.auto_funnels.create_messages.add_message import process_add_message_starting
from states import CreateAutoFunnels, CreateMessageAF


@dp.callback_query_handler(create_af_data.filter(prefix='save'), state=CreateAutoFunnels.choice)
async def process_accept_funnels(call: types.CallbackQuery, state=FSMContext):
    data = await state.get_data()
    funnel = create_auto_funnels(name=data['name'], start_on_week=data['start_on_week'],
                        start_on_day_month=data['start_on_day_month'], fast_start=data['fast_start'],
                        product_id=data['product'],
                        job_buy=data['if_buy'],
                        job_not_buy=data['if_not_buy'])
    # Процесс создания автоворонки
    await state.finish()
    await call.answer('Воронка создана')
    await CreateMessageAF.choice.set()
    await state.update_data(data={'type': 'first', 'funnel_id': funnel.id, 'is_fast_start': funnel.fast_start})
    await process_add_message_starting(call, state, {})


@dp.callback_query_handler(create_af_data.filter(prefix='cancel'), state=CreateAutoFunnels.choice)
async def process_accept_funnels(call: types.CallbackQuery, state=FSMContext):
    await call.answer('Создание воронки отменено')
    await call.message.edit_text('Автоворонки', reply_markup=auto_funnels_menu)
    await state.finish()