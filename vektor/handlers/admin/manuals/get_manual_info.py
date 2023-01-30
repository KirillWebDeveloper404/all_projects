from aiogram import types

from keyboards.inline.admin.create_manual import get_create_manual_kb
from states import CreateManual


async def get_manuals_info(category, name, desc):
    if not name:
        name = 'Нет имени'

    if not desc:
        desc = 'Не имеет описания'

    text = f'<b>{name}</b>\n\n' \
           f'{desc}'

    return text


async def send_manual_info_created(data, message: types.Message, is_delete=False):
    text = await get_manuals_info(data['category'], data['name'], data['desc'])

    if is_delete:
        await message.delete()

    await CreateManual.process.set()
    keyboard = await get_create_manual_kb(data=data)
    await message.answer(text, reply_markup=keyboard)


from utils.db_api.manuals_model import get_manual_by_id


async def get_manuals_info_by_view_admin(manual_id):
    manual = await get_manual_by_id(manual_id)
    text = f'<b>{manual.name}</b>\n\n' \
           f'{manual.desc}'
    return text
