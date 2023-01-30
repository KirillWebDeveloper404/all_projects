from aiogram import types

from loader import dp
from modules.BotKeyboards import list_admin_dt, delete_admin_dt, generate_list_admins_kb, delete_admin_kb
from modules.DataBase import get_admins


@dp.callback_query_handler(list_admin_dt.filter())
async def process_get_view_user(call: types.CallbackQuery, callback_data: dict):
    tg_id = int(callback_data.get('tg_id'))
    if tg_id == call.from_user.id:
        await call.answer(cache_time=1, text='Вы не можете редактировать себя')
        return
    name = callback_data.get('name')
    id = int(callback_data.get('id'))
    phone = callback_data.get('phone')
    text = f'Админ:\nid:{id}\nИмя:{name}\nТелефон:{phone}'
    keyboard = await delete_admin_kb(id, tg_id=tg_id, name=name, phone=phone)
    await call.message.edit_text(text, reply_markup=keyboard)


@dp.callback_query_handler(delete_admin_dt.filter(prefix='back'))
async def process_back_view_admin(call: types.CallbackQuery):
    admins = get_admins()
    keyboard = await generate_list_admins_kb(admins)
    text = 'Список админов:\n\n'
    for admin in admins:
        text += f'Админ:\nid:{admin.id}\nname:{admin.name}\nphone:{admin.phone_number}\n\n'
    text += 'Нажмите на кнопку админа для удаления'
    await call.answer(cache_time=1)
    await call.message.edit_text(text, reply_markup=keyboard)