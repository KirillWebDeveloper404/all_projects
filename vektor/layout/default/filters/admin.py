from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from modules.DataBase import is_admin


class IsAdmin(BoundFilter):
    async def check(self, query: types.InlineQuery) -> bool:
        admin = is_admin(query.from_user.id)
        return admin
