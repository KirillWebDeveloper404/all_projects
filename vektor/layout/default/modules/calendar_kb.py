import datetime
from calendar import monthcalendar
from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from apscheduler.job import Job

from modules.Credentials import UTC_TIME_ZONE

control_months_data = CallbackData("control_months_data", "prefix", "year", "month")
calendar_info_data = CallbackData("calendar_info_data", "prefix", "year", "month", "day")
day_on_month_data = CallbackData("day_on_month_data", "text")


def generate_calendar_kb(year=None, month=None, back='statistics'):
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
        now = datetime.datetime.now(UTC_TIME_ZONE)
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

    inline_keyboard.append([InlineKeyboardButton("« Назад", callback_data=f"{back}_back")])

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


control_months_data_jobs = CallbackData("control_months_data_jobs", "prefix", "year", "month")
calendar_info_data_jobs = CallbackData("calendar_jobs", "prefix", "year", "month", "day", 'have_jobs')


def generate_calendar_jobs_kb(jobs: List[Job], year=None, month=None):
    if year and month:
        year = int(year)
        month = int(month)
        control_months = [
            InlineKeyboardButton(
                text="<", callback_data=control_months_data_jobs.new(prefix="prev", year=f"{year}", month=f"{month}")
            ),
            InlineKeyboardButton(
                text=f"{get_month_text(int(month))} {year}",
                callback_data=control_months_data_jobs.new(prefix="month", year=f"{year}", month=f"{month}"),
            ),
            InlineKeyboardButton(
                text=">", callback_data=control_months_data_jobs.new(prefix="next", year=f"{year}", month=f"{month}")
            ),
        ]
        day_on_month = monthcalendar(year, month)
    else:
        now = datetime.datetime.now(UTC_TIME_ZONE)
        month = now.month
        year = now.year
        control_months = [
            InlineKeyboardButton(
                text="<", callback_data=control_months_data_jobs.new(prefix="prev", year=f"{year}", month=f"{month}")
            ),
            InlineKeyboardButton(
                text=f"{get_month_text(now.month)} {now.year}",
                callback_data=control_months_data_jobs.new(prefix="month", year=f"{year}", month=f"{month}"),
            ),
            InlineKeyboardButton(
                text=">", callback_data=control_months_data_jobs.new(prefix="next", year=f"{year}", month=f"{month}")
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
                job_accept = None
                for job in jobs:
                    job_date = job.next_run_time
                    if job_date.year == year and job_date.month == month and job_date.day == week[i]:
                        job_accept = True
                if job_accept:
                    new_week.append(
                        InlineKeyboardButton(
                            text=f'💌{week[i]}',
                            callback_data=calendar_info_data_jobs.new(
                                prefix="day", year=f"{year}", month=f"{month}", day=f"{week[i]}", have_jobs='yes'
                            ),
                        )
                    )
                else:
                    new_week.append(
                        InlineKeyboardButton(
                            text=week[i],
                            callback_data=calendar_info_data_jobs.new(
                                prefix="day", year=f"{year}", month=f"{month}", day=f"{week[i]}", have_jobs='None'
                            ),
                        )
                    )
            else:
                new_week.append(
                    InlineKeyboardButton(
                        text=" ",
                        callback_data=calendar_info_data_jobs.new(
                            prefix="day", year=f"{year}", month=f"{month}", day="null", have_jobs='None'
                        ),
                    )
                )
            if i == 6:
                inline_keyboard.append(new_week)

    inline_keyboard.append([InlineKeyboardButton("« Назад", callback_data="mailing_schedule_back")])

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
