from utils.db_api.manuals_model import get_manual_by_id


async def get_manuals_info(manual_id):
    manual = await get_manual_by_id(manual_id)
    text = f'<b>{manual.name}</b>\n\n' \
           f'{manual.desc}'
    return text
