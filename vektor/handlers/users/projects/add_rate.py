import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import PAY_TOKEN
from keyboards.inline.add_rates import add_rate_for_create
from keyboards.inline.manage_project import get_manage_project_kb
from loader import dp, bot, bots_manager
from states.create_project import CreateProject
from utils.db_api.projects_model import create_project, change_project_settings
from utils.db_api.rates_model import get_rate_by_id
from utils.db_api.shoplist_model import create_order
import logging

from utils.db_api.transactions import save_transaction
from utils.db_api.users_model import add_balance_for_all_referrals, update_status_is_payment, get_user_by_chat_id


@dp.callback_query_handler(add_rate_for_create.filter(), state=CreateProject.rate)
async def process_add(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=1)
    rate_id = int(callback_data.get('rate_id'))
    user = await get_user_by_chat_id(call.from_user.id)
    rate = await get_rate_by_id(rate_id=rate_id)
    await state.update_data(data={
        'rate_id': rate.id
    })
    price = rate.price * 100
    await call.message.delete()
    await call.message.answer("Создаем проект и форму для оплаты. Ожидайте.")
    data = await state.get_data()
    project = await create_project(
        token=data['token'],
        chat_id=call.from_user.id,
        name=data['name'],
        rate=rate.id
    )
    await bots_manager.add_bot(int(project.id), data['token'], path_layout=rate.path, admin=call.from_user.id)
    await bots_manager.__off_status__(project.id)
    if user.free_active:
        await call.message.answer("Мы создали ваш проект. Теперь вы можете пользоваться им 7 дней.")
        await state.finish()
        return
    else:
        await call.message.answer('Мы создали ваш проект вы сможете его включить после оплаты')

    await state.finish()

    await bot.send_invoice(
        chat_id=call.from_user.id,
        title=rate.name,
        description=rate.desc,
        payload=f'{rate.id}:{project.id}',
        provider_token=PAY_TOKEN,
        start_parameter="2121",
        currency='RUB',
        prices=[types.LabeledPrice(label=rate.name, amount=price)]
    )


@dp.pre_checkout_query_handler()
async def process_checkout(query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(query.id, True)


@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def process_payment(message: types.Message):

    data = message.successful_payment.invoice_payload.split(':')
    amount = message.successful_payment.total_amount/100
    project_id = int(data[1])
    logging.info(project_id)
    await bots_manager.__on_status__(project_id)
    rate_id = int(data[0])
    end_date = datetime.datetime.now() + datetime.timedelta(days=30)
    await change_project_settings(project_id=project_id, is_payment=True, end_date=end_date)
    await update_status_is_payment(message.from_user.id, True)
    await save_transaction(message.from_user.id, amount)

    rate = await get_rate_by_id(rate_id=rate_id)
    text = await bots_manager.get_info_bot(project_id)
    keyboard = await get_manage_project_kb(project_id)
    await create_order(price=rate.price, rate=rate.id, chat_id=message.from_user.id)
    await add_balance_for_all_referrals(chat_id=message.from_user.id, price=rate.price)
    await message.answer(text, reply_markup=keyboard)
