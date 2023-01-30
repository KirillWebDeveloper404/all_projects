import pytz
from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.setting.time_zone import  timezone_data, GenerateInlineKeyboardButtons
from loader import dp, bots_manager
from utils.db_api.users_model import update_utc_timezone, get_user_by_chat_id


@dp.callback_query_handler(timezone_data.filter(pr="back"))
async def setting_back_handler(call: types.CallbackQuery):
    await call.message.edit_text("В главном меню")

@dp.message_handler(text="⚙️ Настройки", state="*")
async def setting_handler(m: types.Message, state: FSMContext):
    markup = GenerateInlineKeyboardButtons()
    user = await get_user_by_chat_id(m.from_user.id)
    if user.utc_timezone:
        await m.answer("🛠 Настройки\n"
                       "Выберите часовой пояс", reply_markup=markup.generate_keyboard(user.utc_timezone))
        return

    await m.answer("🛠 Настройки\n"
                   "Выберите часовой пояс", reply_markup=markup.generate_keyboard_start())


@dp.callback_query_handler(timezone_data.filter(pr="timezone"))
async def setting_time_zone_projects(call: types.CallbackQuery, callback_data: dict):
    timezone = callback_data.get("timezone")
    markup = GenerateInlineKeyboardButtons()
    await update_utc_timezone(call.from_user.id, timezone)
    await bots_manager.__restart_project_and_update_timezone__(utc_timezone=timezone, chat_id=call.from_user.id)
    await call.message.edit_text(text="🛠 Настройки\n"
                                      "Выберите часовой пояс", reply_markup=markup.generate_keyboard(timezone))

