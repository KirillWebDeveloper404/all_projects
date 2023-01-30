from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def get_rate_view_user(club):
    keyboard = InlineKeyboardMarkup()
    if club.channel:
        keyboard.row(InlineKeyboardButton(text='Канал', url=club.channel))
    if club.private_chat:
        keyboard.row(InlineKeyboardButton(text='Чат', url=club.private_chat))
    if not club.channel and club.private_chat:
        return None
    return keyboard
