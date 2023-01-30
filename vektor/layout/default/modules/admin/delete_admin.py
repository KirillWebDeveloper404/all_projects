from aiogram import types

from loader import dp
from modules.BotKeyboards import delete_admin_dt, generate_list_admins_kb, generate_accept_delete_kb, delete_admin_kb
from modules.DataBase import get_admins, delete_admin


@dp.callback_query_handler(delete_admin_dt.filter(prefix='delete'))
async def process_delete_admin(call: types.CallbackQuery, callback_data: dict):
    admin_id = callback_data.get('id')
    name = callback_data.get('name')
    tg_id = int(callback_data.get('tg_id'))
    phone = callback_data.get('phone')
    text = f'Вы точно хотите удалить этого админа?\n\nАдмин:\nid:{admin_id}\nИмя:{name}\nТелефон:{phone}'
    keyboard = await generate_accept_delete_kb(id_admin=admin_id, tg_id=tg_id, name=name, phone=phone)

    await call.answer(cache_time=1)
    await call.message.edit_text(text, reply_markup=keyboard)


@dp.callback_query_handler(delete_admin_dt.filter(prefix='accept_delete'))
async def process_accept_delete_admin(call: types.CallbackQuery, callback_data: dict):
    admin_id = int(callback_data.get('id'))
    delete_admin(admin_id)
    admins = get_admins()
    keyboard = await generate_list_admins_kb(admins)
    text = 'Админ успешно удален\n' \
           'Список админов:\n\n'
    for admin in admins:
        text += f'Админ:\nid:{admin.id}\nname:{admin.name}\\n\n'
    text += 'Нажмите на кнопку админа для удаления'
    await call.answer(cache_time=1)
    await call.message.edit_text(text, reply_markup=keyboard)


@dp.callback_query_handler(delete_admin_dt.filter(prefix='no_delete'))
async def process_back_accept_delete_admin(call: types.CallbackQuery, callback_data: dict):
    tg_id = int(callback_data.get('tg_id'))
    name = callback_data.get('name')
    id = int(callback_data.get('id'))
    phone = callback_data.get('phone')
    text = f'Админ:\nid:{id}\nИмя:{name}\nТелефон:{phone}'
    keyboard = await delete_admin_kb(id, tg_id=tg_id, name=name, phone=phone)
    await call.message.edit_text(text, reply_markup=keyboard)
