import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode, KeyboardButton

import modules.Config as Cfg
from loader import dp, bot
from modules import Methods



# состояния, необходимые для диалога при верификации
from modules.DataBase import is_admin, get_user_april_on_tg_id, register_user_april_start, get_all_auto_funnels, \
    get_first_message_af_by_funnel_id, get_user_by_tg_id, login_new_client, update_phone_number
from utils.functions.register_user_on_funnel import register_user_on_funnel
from utils.functions.send_message_funnel import send_first_message_funnel


class VerState(StatesGroup):
    waiting_for_phone = State()


@dp.message_handler(commands=["start"], state="*")
async def bot_starter(message: types.Message, state: FSMContext):
    args = message.get_args()
    user = get_user_by_tg_id(message.from_user.id)
    auto_funnels = get_all_auto_funnels()

    if not user:
        start_funnel = None
        for funnel in auto_funnels:
            if funnel.name == args:
                start_funnel = funnel.name
                break

        login_new_client(message.from_user.id, "", message.from_user.first_name, start_funnel)


    user_funnel = []
    for funnel in auto_funnels:
        if funnel.name == args:
            is_register = await register_user_on_funnel(funnel_id=funnel.id, chat_id=message.from_user.id)
            if is_register:
                user_funnel.append(funnel.id)
            break
    if user_funnel:
        message_af = get_first_message_af_by_funnel_id(user_funnel[0])
        await send_first_message_funnel(message_id=message_af.id, chat_id=message.chat.id)

