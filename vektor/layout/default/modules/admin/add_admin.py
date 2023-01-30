from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, ForwardedMessageFilter

from loader import dp
from modules.BotKeyboards import add_admin_panel_not_super, admin_dt, admin_manage_dt, admin_manage, \
    employees_kb
from modules.Credentials import ADMINS
from modules.DataBase import get_admin_by_id_one, register_admin, \
    get_user_by_tg_id
from states.add_admin import AddAdmin


@dp.callback_query_handler(admin_dt.filter(prefix="administrator_manage"))
async def get_kb_control_admins(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    # admin = get_admin_by_id_one(call.from_user.id)
    await call.message.delete()
    # print(ADMINS, type(ADMINS))
    if not (str(call.from_user.id) in ADMINS):
        text = "У вас нет доступа к этому функционалу"
        await call.message.answer(text, reply_markup=add_admin_panel_not_super)
        return
    text = "Управление администраторами"
    await call.message.answer(text, reply_markup=admin_manage)


@dp.callback_query_handler(admin_manage_dt.filter(prefix="back"), state="*")
async def process_back_to_add_admin_panel(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.answer(cache_time=1)
    text = "Управление"
    await call.message.edit_text(text, reply_markup=employees_kb)

@dp.callback_query_handler(admin_manage_dt.filter(prefix="add"))
async def process_add_admin(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    text = "Перешлите сообщение из личной переписки боту"
    await call.message.answer(text)
    await AddAdmin.get_admin_id.set()


@dp.message_handler(ForwardedMessageFilter(True), state=AddAdmin.get_admin_id)
async def process_get_admin_phone(message: types.Message, state=FSMContext):
    user = get_user_by_tg_id(message.forward_from.id)

    if user:
        admin = get_admin_by_id_one(user.tg_id)
        if admin:
            text = "Такой админ уже есть!\nВы в управлении администраторами"
            await message.answer(text, reply_markup=admin_manage)
        else:
            register_admin(name=user.name, tg_id=user.tg_id)
            text = "Админ успешно зарегистрирован\nВы в управлении администраторами"
            await message.answer(text, reply_markup=admin_manage)

    else:
        text = "Такого пользователя нет\nВы в управлении администраторами"
        await message.answer(text, reply_markup=admin_manage)

    await state.finish()
