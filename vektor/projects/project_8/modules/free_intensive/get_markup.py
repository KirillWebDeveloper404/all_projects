from modules.BotKeyboards import (
    free_intensive_habits,
    free_intensive_join_chat,
    free_intensive_korset,
    free_intensive_photo_before_after,
    free_intensive_reviews,
    friday_vebinar_kb, free_intensive_vebinar_first, free_intensive_vebinar_last, free_intensive_yashiva,
)


async def get_markup(id):
    if id == 1 or id == 6:
        return free_intensive_join_chat
    elif id == 3:
        return free_intensive_habits
    elif id == 5:
        return free_intensive_reviews
    elif id == 8:
        return free_intensive_photo_before_after
    elif id == 14 or id == 15 or id == 16:
        return free_intensive_korset
    elif id == 13:
        return friday_vebinar_kb
    elif id == 12:
        return free_intensive_yashiva
    else:
        return None


async def get_markup_vebinar(id):
    if id == 3 or id == 4:
        return free_intensive_vebinar_last
    if id ==1 or id == 2:
        return free_intensive_vebinar_first
    else:
        return None
