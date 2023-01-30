from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class ReferralStart(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        args = message.get_args()
        if args:
            return args.startswith('ref')
        else:
            return False
