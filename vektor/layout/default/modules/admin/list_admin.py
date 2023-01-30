from aiogram import types

from loader import dp
from modules.BotKeyboards import add_admin_panel_not_super, admin_manage_dt, admin_manage, \
    generate_list_admins_kb, list_admin_dt
from modules.DataBase import get_admin_by_id_one, get_admins


@dp.callback_query_handler(admin_manage_dt.filter(prefix='list'))
async def process_get_list_admins(call: types.CallbackQuery):
    admins = get_admins()
    keyboard = await generate_list_admins_kb(admins)
    text = 'Список админов:\n\n'
    for admin in admins:
        text += f'Админ:\nid:{admin.id}\nname:{admin.name}\n\n'
    text += 'Нажмите на кнопку админа для удаления'
    await call.answer(cache_time=1)
    await call.message.edit_text(text, reply_markup=keyboard)


@dp.callback_query_handler(list_admin_dt.filter(id='back'))
async def process_back_to_admin_manage(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    admin = get_admin_by_id_one(call.from_user.id)
    text = "Управление администраторами"

    if not admin:
        await call.message.edit_text(text, reply_markup=admin_manage)
        return
    if admin.name != "Суперадмин":
        text = "У вас нет доступа к этому функционалу"
        await call.message.edit_text(text, reply_markup=add_admin_panel_not_super)
        return

    await call.message.edit_text(text, reply_markup=admin_manage)
