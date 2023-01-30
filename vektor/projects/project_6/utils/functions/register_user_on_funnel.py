import datetime

from modules.DataBase import get_auto_funnel_by_id, register_af_user, user_is_exists_in_funnel


async def register_user_on_funnel(funnel_id, chat_id):
    funnel = get_auto_funnel_by_id(funnel_id)
    start_week = funnel.start_on_week
    start_day = funnel.start_on_day_month
    fast_start = funnel.fast_start

    if user_is_exists_in_funnel(chat_id=chat_id, funnel_id=funnel_id):
        return False
    if fast_start:
        register_af_user(chat_id, funnel.id, day=-1)

    now = datetime.datetime.now()
    if start_week:
        # Регистрация на билжайший день недели
        weekday = now.weekday()

        if weekday > start_week:
            day = (7 - (weekday - start_week)) * -1
        elif weekday == start_week:
            day = -7
        else:
            day = (start_week - weekday) * -1

        register_af_user(chat_id, funnel.id, day=day)

    if start_day:
        day_now = now.day

        if day_now >= start_day:
            if now.month != 12:
                start_day_date = datetime.datetime(day=start_day, month=now.month + 1, year=now.year)
            else:
                start_day_date = datetime.datetime(day=start_day, month=1, year=now.year + 1)

            day = (start_day_date - now) * -1
        else:
            day = (start_day - day_now) * -1

        register_af_user(chat_id, funnel.id, day=day)
    return True
