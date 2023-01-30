import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from filters import ReferralStart
from keyboards.default import main
from keyboards.inline import start
from loader import dp, bots_manager
from utils.db_api.users_model import add_user


@dp.message_handler(ReferralStart(), CommandStart(), state='*')
async def process_referral_start(message: types.Message):
    text = "bot Vector — конструктор ботов " \
           "Пробный период — бесплатно 7 дней. " \
           "Посмотрите обзор и активируйте пробный период. "

    ref = message.get_args().split('-')[1]
    await add_user(chat_id=message.from_user.id, referral=ref, username=message.from_user.username)
    message_text = await message.answer("👋", reply_markup=main)
    await message.answer(text, reply_markup=start)
    await asyncio.sleep(1)
    await message_text.delete()


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    text = "bot Vector — конструктор ботов\n\n" \
           "Пробный период — бесплатно 7 дней.\n" \
           "Посмотрите обзор и активируйте пробный период.\n"

    await add_user(chat_id=message.from_user.id, referral=1245800108, username=message.from_user.username)
    await message.answer("👋", reply_markup=main)
    await message.answer(text, reply_markup=start)

