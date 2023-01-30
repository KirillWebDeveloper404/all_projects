from aiogram import Dispatcher, types


async def set_default_command(dp: Dispatcher):
    await dp.bot.set_my_commands([
        types.BotCommand('start', 'Перезапустить бот'),
    ])
