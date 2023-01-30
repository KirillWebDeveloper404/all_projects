import datetime
from calendar import monthcalendar
from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from apscheduler.job import Job

control_months_data = CallbackData("cmd_funnel", "prefix", "year", "month")
calendar_info_data = CallbackData("cal_info_dt_funnel", "prefix", "year", "month", "day")
day_on_month_data = CallbackData("day_on_month_data_funnel", "text")


def generate_calendar_kb(year=None, month=None):
    if year and month:
        year = int(year)
        month = int(month)
        control_months = [
            InlineKeyboardButton(
                text="<", callback_data=control_months_data.new(prefix="prev", year=f"{year}", month=f"{month}")
            ),
            InlineKeyboardButton(
                text=f"{get_month_text(int(month))} {year}",
                callback_data=calendar_info_data.new(prefix="month", year=f"{year}", month=f"{month}", day="not"),
            ),
            InlineKeyboardButton(
                text=">", callback_data=control_months_data.new(prefix="next", year=f"{year}", month=f"{month}")
            ),
        ]
        day_on_month = monthcalendar(year, month)
    else:
        now = datetime.datetime.now()
        month = now.month
        year = now.year
        control_months = [
            InlineKeyboardButton(
                text="<", callback_data=control_months_data.new(prefix="prev", year=f"{year}", month=f"{month}")
            ),
            InlineKeyboardButton(
                text=f"{get_month_text(now.month)} {now.year}",
                callback_data=calendar_info_data.new(prefix="month", year=f"{year}", month=f"{month}", day="not"),
            ),
            InlineKeyboardButton(
                text=">", callback_data=control_months_data.new(prefix="next", year=f"{year}", month=f"{month}")
            ),
        ]
        day_on_month = monthcalendar(now.year, now.month)

    inline_keyboard = [
        control_months,
        [
            InlineKeyboardButton("пн", callback_data=day_on_month_data.new(text="понедельник")),
            InlineKeyboardButton("вт", callback_data=day_on_month_data.new(text="вторник")),
            InlineKeyboardButton("ср", callback_data=day_on_month_data.new(text="среда")),
            InlineKeyboardButton("чт", callback_data=day_on_month_data.new(text="четверг")),
            InlineKeyboardButton("пт", callback_data=day_on_month_data.new(text="пятница")),
            InlineKeyboardButton("сб", callback_data=day_on_month_data.new(text="суббота")),
            InlineKeyboardButton("вс", callback_data=day_on_month_data.new(text="воскресенье")),
        ],
    ]

    for week in day_on_month:
        new_week = []
        for i in range(len(week)):
            if week[i] != 0:
                new_week.append(
                    InlineKeyboardButton(
                        text=week[i],
                        callback_data=calendar_info_data.new(
                            prefix="day", year=f"{year}", month=f"{month}", day=f"{week[i]}"
                        ),
                    )
                )
            else:
                new_week.append(
                    InlineKeyboardButton(
                        text=" ",
                        callback_data=calendar_info_data.new(
                            prefix="day", year=f"{year}", month=f"{month}", day="null"
                        ),
                    )
                )
            if i == 6:
                inline_keyboard.append(new_week)

    inline_keyboard.append([InlineKeyboardButton("« Назад", callback_data="statistics_funnel_back")])

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def get_month_text(month):
    months = [
        "Январь",
        "Февраль",
        "Март",
        "Апрель",
        "Май",
        "Июнь",
        "Июль",
        "Август",
        "Сентябрь",
        "Октябрь",
        "Ноябрь",
        "Декабрь",
    ]

    return months[month - 1]


if __name__ == "__main__":
    generate_calendar_kb()
