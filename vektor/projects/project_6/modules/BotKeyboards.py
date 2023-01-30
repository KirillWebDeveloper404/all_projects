"""
тут кнопки и функции, генерирующие их
"""

import calendar as clndr
import copy
from datetime import date
from typing import List, Union

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, user
from aiogram.utils.callback_data import CallbackData

from loader import scheduler
from modules import DataBase as db
from modules.DataBase import get_user_rate

client_main = ReplyKeyboardMarkup(resize_keyboard=True)
client_main.row(KeyboardButton("🧘 Мои занятия"), KeyboardButton("🛍 Магазин"))
client_main.row(KeyboardButton("✨ О школе"), KeyboardButton("🆘 Помощь"))

client_main_admin = ReplyKeyboardMarkup(resize_keyboard=True)
client_main_admin.row(KeyboardButton("🧘 Мои занятия"), KeyboardButton("🛍 Магазин"))
client_main_admin.row(KeyboardButton("✨ О школе"), KeyboardButton("🆘 Помощь"))
client_main_admin.row(KeyboardButton("Панель админа"))

subscribe_inst = InlineKeyboardMarkup()
subscribe_inst.add(
    InlineKeyboardButton(
        "📲 Подписаться на мой инстаграм", url="https://www.instagram.com/p/CHIxKyDhZCR/?igshid=1p94vkwswnzcc"
    )
)
subscribe_inst.add(InlineKeyboardButton("📺 Получить подборку видео", callback_data="collection_1"))
subscribe_inst.add(InlineKeyboardButton("👣 Бесплатный интенсив 5 шагов", callback_data="free_intensive_start"))
subscribe_inst.add(InlineKeyboardButton("⭐️ Платный интенсив Я ЖИВА!", callback_data="pay_intensive_start"))

questionnaire_1 = InlineKeyboardMarkup()
questionnaire_1.row(
    InlineKeyboardButton(
        "📲 Подписаться на мой инстаграм", url="https://www.instagram.com/p/CHIxKyDhZCR/?igshid=1p94vkwswnzcc"
    )
)
questionnaire_1.row(InlineKeyboardButton("🔎 Пройти тестирование", callback_data="questionnaire_1"))

questionnaire_april = InlineKeyboardMarkup()
questionnaire_april.row(
    InlineKeyboardButton(
        "📲 Подписаться на мой инстаграм", url="https://www.instagram.com/p/CHIxKyDhZCR/?igshid=1p94vkwswnzcc"
    )
)
questionnaire_april.row(InlineKeyboardButton("🔎 Пройти тестирование", callback_data="questionnaire_april_1"))


def gen_client_main():
    kb = copy.deepcopy(client_main)
    return kb


# faq buttons
client_help = InlineKeyboardMarkup()
client_help.row(InlineKeyboardButton(text="✍️ Написать в поддержку", callback_data="help_write_to_help"))
client_help.row(InlineKeyboardButton(text="💵 Не могу оплатить занятие", callback_data="help_write_to_help"))
client_help.row(InlineKeyboardButton(text="❄️ Заморозить абонемент", callback_data="help_freeze"))
client_help.row(InlineKeyboardButton(text="🤷‍♀️ Не получилось посетить занятие", callback_data="help_write_to_help"))
client_help.row(
    InlineKeyboardButton(text="👀 Как смотреть оставшиеся занятия по абонементу", callback_data="help_write_to_help")
)

# user account

client_cabinet = InlineKeyboardMarkup(row_width=2)
client_cabinet.row(InlineKeyboardButton("🛒 Покупки", callback_data="client_cabinet_shop"))
client_cabinet.row(InlineKeyboardButton("✍️ Написать куратору", callback_data="client_cabinet_curator"))
# client_lk.row(InlineKeyboardButton("🏦 История транзакций", callback_data="client_cabinet_transactions"))


activate_lk = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Перейти к активации", callback_data="activate_lk")]]
)

get_number = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton("Поделиться номером", request_contact=True)], [KeyboardButton("« Назад")]],
    resize_keyboard=True,
)


def client_lk_gen(is_admin):
    ret = copy.deepcopy(client_cabinet)
    if is_admin:
        ret.row(InlineKeyboardButton("🔐 Панель администратора", callback_data="admin_main"))
    return ret


client_passw_verify = ReplyKeyboardMarkup(one_time_keyboard=True).add(
    KeyboardButton("Подтвердить номер телефона", request_contact=True)
)


def gen_client_timetable():
    client_timetable = InlineKeyboardMarkup()
    client_timetable.row(
        InlineKeyboardButton("Бесплатные события", callback_data="timetable_free_classes"),
        InlineKeyboardButton("Календарь", callback_data="timetable_calendar"),
    )
    for tchr in db.get_teachers():
        if tchr.tg_id is not None:
            client_timetable.row(
                InlineKeyboardButton(tchr.name, callback_data="timetable_teacherbutton:" + tchr.phone_number)
            )
    return client_timetable


def days_of_week():
    return [InlineKeyboardButton(d, callback_data="no") for d in ("Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс")]


def gen_month_for_admin(chat, dt):
    ret = InlineKeyboardMarkup(row_width=7)
    ret.add(InlineKeyboardButton(f"{month_from_num(dt.month)} {dt.year}", callback_data="no"))
    ret.row(*days_of_week())
    dt = date(dt.year, dt.month, 1)
    max_day = clndr.monthrange(dt.year, dt.month)[1]
    day = 1
    for i in range(dt.weekday()):
        ret.insert(InlineKeyboardButton(" ", callback_data="no"))
    for i in range(dt.weekday(), 7):
        if db.get_events_by_date(date(dt.year, dt.month, day)):
            ret.insert(InlineKeyboardButton("|" + str(day) + "|", callback_data=f"dt_admin{dt.year}.{dt.month}.{day}"))
        else:
            ret.insert(InlineKeyboardButton(str(day), callback_data=f"dt_admin{dt.year}.{dt.month}.{day}"))
        day += 1
    dy = day
    for i in range(4 * 7):
        if dy != " " and db.get_events_by_date(date(dt.year, dt.month, dy)):
            ret.insert(InlineKeyboardButton("|" + str(dy) + "|", callback_data=f"dt_admin{dt.year}.{dt.month}.{day}"))
        else:
            ret.insert(InlineKeyboardButton(str(dy), callback_data=f"dt{dt.year}.{dt.month}.{day}"))
        if day < max_day:
            day += 1
            dy += 1
        else:
            dy = " "
    ret.row(
        InlineKeyboardButton("<", callback_data=f"dtprev_month_for_admin:{chat}:{dt.year}.{dt.month}"),
        InlineKeyboardButton("   ", callback_data="no"),
        InlineKeyboardButton(">", callback_data=f"dtnext_month_for_admin:{chat}:{dt.year}.{dt.month}"),
    )
    return ret


def gen_month_for_teacher(chat, dt, user_id):
    ret = InlineKeyboardMarkup(row_width=7)
    ret.add(InlineKeyboardButton(f"{month_from_num(dt.month)} {dt.year}", callback_data="no"))
    ret.row(*days_of_week())
    dt = date(dt.year, dt.month, 1)
    max_day = clndr.monthrange(dt.year, dt.month)[1]
    day = 1
    for i in range(dt.weekday()):
        ret.insert(InlineKeyboardButton(" ", callback_data="no"))
    for i in range(dt.weekday(), 7):
        if db.get_events_by_teacher(date(dt.year, dt.month, day), user_id):
            ret.insert(
                InlineKeyboardButton("|" + str(day) + "|", callback_data=f"dt_teacher{dt.year}.{dt.month}.{day}")
            )
        else:
            ret.insert(InlineKeyboardButton(str(day), callback_data=f"dt{dt.year}.{dt.month}.{day}"))
        day += 1
    dy = day
    for i in range(4 * 7):
        if dy != " " and db.get_events_by_teacher(date(dt.year, dt.month, dy), user_id):
            ret.insert(InlineKeyboardButton("|" + str(dy) + "|", callback_data=f"dt_teacher{dt.year}.{dt.month}.{day}"))
        else:
            ret.insert(InlineKeyboardButton(str(dy), callback_data=f"dt{dt.year}.{dt.month}.{day}"))
        if day < max_day:
            day += 1
            dy += 1
        else:
            dy = " "
    ret.row(
        InlineKeyboardButton("<", callback_data=f"dtprev_month_for_teacher:{chat}:{dt.year}.{dt.month}"),
        InlineKeyboardButton("   ", callback_data="no"),
        InlineKeyboardButton(">", callback_data=f"dtnext_month_for_teacher:{chat}:{dt.year}.{dt.month}"),
    )
    return ret


def gen_month(chat, dt, user_id):
    """
    создает инлайн календарик для клиента с колбэками на кнопках, которые выводят список
    занятий (персональных тоже) и семинаров в конкретный день
    входные параметры
    dt - дата (важен только месяц и год)
    user_id - телеграм айди пользователя
    chat - айди сообщения в чате, чтобы при смене месяца - редактировать сообщение
    а не создавать новое
    """
    ret = InlineKeyboardMarkup(row_width=7)
    ret.add(InlineKeyboardButton(f"{month_from_num(dt.month)} {dt.year}", callback_data="no"))
    ret.row(*days_of_week())
    dt = date(dt.year, dt.month, 1)
    max_day = clndr.monthrange(dt.year, dt.month)[1]
    day = 1
    # insert empty buttons in the beginning of the month when 1st day starts from arbitrary day of week
    for i in range(dt.weekday()):
        ret.insert(InlineKeyboardButton(" ", callback_data="no"))

    for i in range(dt.weekday(), 7):
        user_events = db.get_events_by_client(date(dt.year, dt.month, day), user_id)
        seminars = db.get_seminar_by_date(date(dt.year, dt.month, day))
        emoji = ""
        if user_events:
            emoji = "🧘🏻‍♀️"
        elif seminars:
            emoji = "📚"

        if user_events or seminars:
            ret.insert(InlineKeyboardButton(f"{day}{emoji}", callback_data=f"dt{dt.year}.{dt.month}.{day}"))
        else:
            ret.insert(InlineKeyboardButton(f"{day}", callback_data=f"dt{dt.year}.{dt.month}.{day}"))
        day += 1
    dy = day
    for i in range(4 * 7):
        # empty cell
        if dy == " ":
            ret.insert(InlineKeyboardButton(str(dy), callback_data=f"dt{dt.year}.{dt.month}.{day}"))
        # user events
        elif db.get_events_by_client(date(dt.year, dt.month, dy), user_id):
            ret.insert(InlineKeyboardButton(f"{dy}🧘🏻‍♀️", callback_data=f"dt{dt.year}.{dt.month}.{day}"))
        # seminars
        elif db.get_seminar_by_date(date(dt.year, dt.month, dy)):
            ret.insert(InlineKeyboardButton(f"{dy}📚", callback_data=f"dt{dt.year}.{dt.month}.{day}"))
        # date without events or seminars
        else:
            ret.insert(InlineKeyboardButton(str(dy), callback_data=f"dt{dt.year}.{dt.month}.{day}"))
        if day < max_day:
            day += 1
            dy += 1
        else:
            dy = " "
    ret.row(
        InlineKeyboardButton("<", callback_data=f"dtprev_month:{chat}:{dt.year}.{dt.month}"),
        InlineKeyboardButton("   ", callback_data="no"),
        InlineKeyboardButton(">", callback_data=f"dtnext_month:{chat}:{dt.year}.{dt.month}"),
    )
    return ret


def gen_month_date_chose(chat, dt):
    ret = InlineKeyboardMarkup(row_width=7)
    ret.add(InlineKeyboardButton(f"{month_from_num(dt.month)} {dt.year}", callback_data="no"))
    ret.row(*days_of_week())
    dt = date(dt.year, dt.month, 1)
    max_day = clndr.monthrange(dt.year, dt.month)[1]
    day = 1
    for i in range(dt.weekday()):
        ret.insert(InlineKeyboardButton(" ", callback_data="no"))
    for i in range(dt.weekday(), 7):
        ret.insert(InlineKeyboardButton(str(day), callback_data=f"choose_date{dt.year}.{dt.month}.{day}"))
        day += 1
    dy = day
    for i in range(4 * 7):
        ret.insert(InlineKeyboardButton(str(dy), callback_data=f"choose_date{dt.year}.{dt.month}.{day}"))
        if day < max_day:
            day += 1
            dy += 1
        else:
            dy = " "
    ret.row(
        InlineKeyboardButton("<", callback_data=f"dtprev_month_date_chose:{chat}:{dt.year}.{dt.month}"),
        InlineKeyboardButton("   ", callback_data="no"),
        InlineKeyboardButton(">", callback_data=f"dtnext_month_date_chose:{chat}:{dt.year}.{dt.month}"),
    )
    return ret


def month_from_num(n):
    months = {
        k: v
        for k, v in zip(
            range(1, 13),
            (
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
            ),
        )
    }
    return months[n]


# =========================================Friday Vebinar===============================================

friday_vebinar_data = CallbackData("friday_vebinar", "prefix")

friday_vebinar_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Буду в 14:00", callback_data=friday_vebinar_data.new(prefix="14-00"))],
        [InlineKeyboardButton("Буду в 19:00", callback_data=friday_vebinar_data.new(prefix="19-00"))],
    ]
)

# =========================================ADMIN=PANEL===============================================


admin_dt = CallbackData("administrator_panel", "prefix")

admin_main = InlineKeyboardMarkup(row_width=1)
# admin_main.row(
#     InlineKeyboardButton("Добавить админа", callback_data="admin_add"),
#     InlineKeyboardButton("Список админов", callback_data="admin_list"),
# )

admin_main.row(
    InlineKeyboardButton("✅ Автоворонки", callback_data=admin_dt.new(prefix="auto_funnels")),
    InlineKeyboardButton("👩‍💻 Сотрудники", callback_data=admin_dt.new(prefix="employees")),
)

admin_main.row(
    InlineKeyboardButton("❗️Квизы", callback_data=admin_dt.new(prefix="tests")),
    InlineKeyboardButton("👩 Пользователи", callback_data=admin_dt.new(prefix="users")),
)
admin_main.row(
    InlineKeyboardButton("📩 Рассылка", callback_data=admin_dt.new(prefix="mailing")),
    InlineKeyboardButton("📊 Статистика", callback_data=admin_dt.new(prefix="statistics")),
)
# admin_main.row(InlineKeyboardButton("🎥 Медиа (разработчикам)", callback_data="admin_section_video"))

# =========================================Keyboards Employees===============================================
employees_dt = CallbackData("manage_employees", "prefix")
employees_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("🙋Администраторы", callback_data=admin_dt.new(prefix="administrator_manage"))],
        [InlineKeyboardButton("« Назад", callback_data=employees_dt.new(prefix="back"))],
    ]
)

# =========================================Keyboards Mailing===============================================
mailing_kb_dt = CallbackData("mailing_kb", "prefix")
mailing_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("⚡️Мгновенная", callback_data=mailing_kb_dt.new(prefix="now_send"))],
        [InlineKeyboardButton("📆 По дате", callback_data=mailing_kb_dt.new(prefix="date_send"))],
        [InlineKeyboardButton("🔁 Повторяющаяся", callback_data=mailing_kb_dt.new(prefix="every_send"))],
        [InlineKeyboardButton("🧾 Расписание заданий", callback_data=admin_dt.new(prefix="list_jobs"))],
        [InlineKeyboardButton("« Назад", callback_data=mailing_kb_dt.new(prefix="back"))],
    ]
)

every_mailing_dt = CallbackData("every_mailing", "prefix")
every_mailing = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Каждый день", callback_data=every_mailing_dt.new(prefix="day"))],
        [InlineKeyboardButton("Еженедельно", callback_data=every_mailing_dt.new(prefix="week"))],
        [InlineKeyboardButton("Каждый месяц", callback_data=every_mailing_dt.new(prefix="month"))],
    ]
)

every_mailing_week_dt = CallbackData("every_mailing_week", "prefix")
every_mailing_week = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Каждый понедельник", callback_data=every_mailing_week_dt.new(prefix="0"))],
        [InlineKeyboardButton("Каждый вторник", callback_data=every_mailing_week_dt.new(prefix="1"))],
        [InlineKeyboardButton("Каждую среду", callback_data=every_mailing_week_dt.new(prefix="2"))],
        [InlineKeyboardButton("Каждый четверг", callback_data=every_mailing_week_dt.new(prefix="3"))],
        [InlineKeyboardButton("Каждую пятницу", callback_data=every_mailing_week_dt.new(prefix="4"))],
        [InlineKeyboardButton("Каждую субботу", callback_data=every_mailing_week_dt.new(prefix="5"))],
        [InlineKeyboardButton("Каждое воскресенье", callback_data=every_mailing_week_dt.new(prefix="6"))],
    ]
)

date_send_kb_dt = CallbackData("date_mailing", "prefix")
date_mailing_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Создать рассылку", callback_data=date_send_kb_dt.new(prefix="ok"))],
        [InlineKeyboardButton("Отменить", callback_data=date_send_kb_dt.new(prefix="no"))],
    ]
)
admin_shop_data = CallbackData("administrator_shop", "prefix")
admin_shop = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("🏷 Категории", callback_data=admin_shop_data.new(prefix="category")),
            InlineKeyboardButton("📦 Товары", callback_data=admin_shop_data.new(prefix="products")),
        ],
        [InlineKeyboardButton("« Назад", callback_data=admin_shop_data.new(prefix="back")), ],
    ]
)
admin_shop_category_data = CallbackData("administrator_shop_category", "prefix")
shop_category_data = CallbackData('shop_category_data', 'prefix')
admin_shop_category = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("➕ Добавить", callback_data="admin_add_category"), ],
        [InlineKeyboardButton("➖ Удалить", callback_data="admin_delete_category"), ],
        [InlineKeyboardButton("✏️ Изменить", callback_data=shop_category_data.new(prefix='edit')), ],
        [InlineKeyboardButton("« Назад", callback_data=admin_shop_category_data.new(prefix="back")), ],
    ]
)

admin_shop_product_data = CallbackData("administrator_shop_product", "prefix")
admin_shop_product = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("➕ Добавить", callback_data="admin_add_product"), ],
        [InlineKeyboardButton("➖ Удалить", callback_data="admin_delete_product"), ],
        [InlineKeyboardButton("✏️ Изменить", callback_data="admin_edit_product")],
        [InlineKeyboardButton("« Назад", callback_data=admin_shop_product_data.new(prefix="back")), ],
    ]
)

admin_mailing_data = CallbackData("administarator_mailing_data", "prefix")
admin_course = InlineKeyboardMarkup()
admin_course.row(InlineKeyboardButton("Добавить курс", callback_data="admin_add_course"), )


async def get_admin_mailing():
    admin_mailing = InlineKeyboardMarkup(row_width=2)
    admin_mailing.row(
        InlineKeyboardButton("Всем пользователям", callback_data="all"),
        # InlineKeyboardButton("Прошедшим входное тестирование", callback_data="entrance_test"),
    )
    # admin_mailing.row(
    #     InlineKeyboardButton("Не мамам", callback_data="not_moms"),
    #     InlineKeyboardButton("Беременным", callback_data="pregnant"),
    #     InlineKeyboardButton("Мамам", callback_data="moms"),
    # )
    # admin_mailing.row(
    #     InlineKeyboardButton("1я стадия", callback_data="first_stage"),
    #     InlineKeyboardButton("2я стадия", callback_data="second_stage"),
    #     InlineKeyboardButton("3я стадия", callback_data="third_stage"),
    # )
    # admin_mailing.row(
    #     InlineKeyboardButton("Запуск апрель", callback_data="april_start"),
    # )
    for product in db.get_segment_products():
        admin_mailing.row(
            InlineKeyboardButton(f"Не купившие {product.name}", callback_data=f"not_bought_product_{product.id}")
        )

    for product in db.get_not_deleted_products():
        admin_mailing.row(
            InlineKeyboardButton(f"Купившие продукт {product.name}", callback_data=f"bought_product_{product.id}")
        )

    for funnel in db.get_all_auto_funnels():
        admin_mailing.row(
            InlineKeyboardButton(f"воронка {funnel.name}", callback_data=f"funnel_{funnel.id}")
        )

    admin_mailing.row(InlineKeyboardButton("« Назад", callback_data=admin_mailing_data.new(prefix="back")))
    return admin_mailing


# ==================== Клавиатура для управления администраторами ===========================
admin_manage_dt = CallbackData("administrator_management", "prefix")

admin_manage = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("➕ Добавить", callback_data=admin_manage_dt.new(prefix="add"))],
        [InlineKeyboardButton("📝 Список", callback_data=admin_manage_dt.new(prefix="list"))],
        [InlineKeyboardButton("« Назад", callback_data=admin_manage_dt.new(prefix="back"))],
    ]
)

add_admin_panel_not_super = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton("« Назад", callback_data=admin_manage_dt.new(prefix="back"))], ]
)

list_admin_dt = CallbackData("list_admin", "id", "tg_id", "name", "phone")


async def generate_list_admins_kb(admins: list):
    admins_kb = []
    for admin in admins:

        admins_kb.append(
            [
                InlineKeyboardButton(
                    f"id:{admin.id} name:{admin.name}",
                    callback_data=list_admin_dt.new(
                        id=f"{admin.id}", tg_id=f"{admin.tg_id}", name=f"{admin.name}", phone=f"None"
                    ),
                )
            ]
        )
    admins_kb.append(
        [
            InlineKeyboardButton(
                "« Назад", callback_data=list_admin_dt.new(id="back", tg_id="None", name="None", phone="None")
            )
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=admins_kb)


delete_admin_dt = CallbackData("delete_admin", "prefix", "id", "tg_id", "name", "phone")


async def delete_admin_kb(id_admin, tg_id, name, phone):
    delete_admin_btn = [
        [
            InlineKeyboardButton(
                text="➖ Удалить",
                callback_data=delete_admin_dt.new(
                    prefix="delete", id=f"{id_admin}", tg_id=tg_id, name=name, phone=phone
                ),
            )
        ],
        [
            InlineKeyboardButton(
                text="« Назад",
                callback_data=delete_admin_dt.new(prefix="back", id="None", tg_id=tg_id, name=name, phone=phone),
            )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=delete_admin_btn)


async def generate_accept_delete_kb(id_admin, tg_id, name, phone):
    delete_admin_btn = [
        [
            InlineKeyboardButton(
                text="Да",
                callback_data=delete_admin_dt.new(
                    prefix="accept_delete", id=f"{id_admin}", tg_id=tg_id, name=name, phone=phone
                ),
            )
        ],
        [
            InlineKeyboardButton(
                text="Нет",
                callback_data=delete_admin_dt.new(
                    prefix="no_delete", id=f"{id_admin}", tg_id=tg_id, name=name, phone=phone
                ),
            )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=delete_admin_btn)


admin_all_products = InlineKeyboardMarkup()
for product in db.get_all_products():
    admin_all_products.row(InlineKeyboardButton(product.name, callback_data=f"product_curator_{product.id}"))

not_deleted_products = InlineKeyboardMarkup()
for product in db.get_not_deleted_products():
    not_deleted_products.row(
        InlineKeyboardButton(product.name, callback_data=f"not_deleted_product_curator_{product.id}")
    )


def generate_product_by_curator(curator_id):
    curator_all_products = InlineKeyboardMarkup()
    for products in db.get_products_by_curator(curator_id):
        if products:
            curator_all_products.row(
                InlineKeyboardButton(products.name, callback_data=f"rm_product_by_curator_{products.id}")
            )
    return curator_all_products


# ==================== Клавиатура для возращения из статистики ===========================
statistics_kb = InlineKeyboardMarkup(row_width=1)
statistics_kb.row(InlineKeyboardButton("« Назад", callback_data="statistics_back"))

curator_changes = InlineKeyboardMarkup()
curator_changes_data = CallbackData("curator_changes_data", "prefix")
curator_changes.row(InlineKeyboardButton("📝 Список кураторов", callback_data="admin_main_curator_list"))
curator_changes.row(InlineKeyboardButton("➕ Добавить", callback_data="admin_main_curator_add"))
curator_changes.row(InlineKeyboardButton("➖ Удалить", callback_data="admin_main_curator_delete"))
curator_changes.row(InlineKeyboardButton("✏️ Изменить", callback_data="admin_main_curator_edit"))
curator_changes.row(InlineKeyboardButton("« Назад", callback_data=curator_changes_data.new(prefix="back")))

media_dt = CallbackData("administrator_media_add", "prefix")

admin_video = InlineKeyboardMarkup(row_width=2)
admin_video.row(
    InlineKeyboardButton("📺 Видео", callback_data="admin_add_video"),
    InlineKeyboardButton("🎞 Анимация", callback_data="admin_add_gif"),
)
admin_video.row(
    InlineKeyboardButton("🔈 Аудио", callback_data=media_dt.new(prefix="audio")),
    InlineKeyboardButton("📸 Фото", callback_data="admin_add_photo"),
)
admin_video.row(
    InlineKeyboardButton("🗂 Документ", callback_data=media_dt.new(prefix="document")),
)
admin_video.row(InlineKeyboardButton("« Назад", callback_data=media_dt.new(prefix="back")), )
# ==================== Клавиатура бесплатного интенсива ===========================
free_intensive_data = CallbackData("free_intensive", "filter")

buy_course = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Хочу красивый животик 💃", url="https://yoga-roggelin.ru/shiva"), ],
        [InlineKeyboardButton("Оставить всё как есть 😬", url="https://yoga-roggelin.ru/shiva"), ],
    ]
)
buy_course_2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Хочу красивый животик 💃", url="https://yoga-roggelin.ru/shiva")]
    ]
)

intensive_invite = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Присоединиться 👉🏻", callback_data=free_intensive_data.new(filter="start"))]]
)

free_intensive_join_chat = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton("Перейти на канал", url="https://t.me/joinchat/U7BLXlQbShLy76RS")]]
)

free_intensive_habits = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("тянет на сладкое", callback_data=free_intensive_data.new(filter="habits")), ],
        [InlineKeyboardButton("вечерний жор", callback_data=free_intensive_data.new(filter="habits"))],
        [InlineKeyboardButton("тяга к мучному", callback_data=free_intensive_data.new(filter="habits")), ],
        [InlineKeyboardButton("катастрофическая лень", callback_data=free_intensive_data.new(filter="habits"))],
    ]
)

free_intensive_vebinar_last = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Ссылка на трансляцию", url="https://start.bizon365.ru/room/16929/YR__Korset"), ],
    ]
)

free_intensive_vebinar_first = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Ссылка на трансляцию", url="https://start.bizon365.ru/room/16929/YR_Korset"), ],
    ]
)

free_intensive_korset = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton("Подробнее☝️", url="https://yoga-roggelin.ru/korsett")]]
)

free_intensive_yashiva = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton("Подробнее☝️", url="https://yoga-roggelin.ru/shiva")]]
)

free_intensive_habits_2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("1", callback_data=free_intensive_data.new(filter="habits_2")), ],
        [InlineKeyboardButton("2", callback_data=free_intensive_data.new(filter="habits_2"))],
        [InlineKeyboardButton("3", callback_data=free_intensive_data.new(filter="habits_2"))],
    ]
)
free_intensive_reviews = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Посмотреть отзывы", callback_data=free_intensive_data.new(filter="reviews")), ],
    ]
)

free_intensive_photo_before_after = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Фото до-после", callback_data=free_intensive_data.new(filter="reviews_after_before")), ],
    ]
)

about_school = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton("👉 Подробнее о школе", url="https://yoga-roggelin.ru/")]]
)


# admin_main.row(
#     InlineKeyboardButton("Добавить поддержку", callback_data="help_add"),
#     InlineKeyboardButton("Список поддержки", callback_data="help_list"),
# )
# admin_main.add(
#     InlineKeyboardButton("Переводы учителям", callback_data="teachers_show_statistics"),
#     InlineKeyboardButton("Описание: йога тур", callback_data="help_yoga_tour_desc"),
# )
# admin_main.add(
#     InlineKeyboardButton("Добавить промокод", callback_data="promo_add"),
#     InlineKeyboardButton("Список промокодов", callback_data="promo_list"),
# )
# admin_main.add(
#     InlineKeyboardButton("Добавить видео урок", callback_data="videos_add"),
#     InlineKeyboardButton("Список видео уроков", callback_data="videos_editlist"),
# )
# admin_main.add(
#     InlineKeyboardButton("Добавить видео курс", callback_data="course_add"),
#     InlineKeyboardButton("Список видео курсов", callback_data="course_editlist"),
# )
# admin_main.add(
#     InlineKeyboardButton("Добавить семинар", callback_data="seminar_add"),
#     InlineKeyboardButton("Информация о семинаре", callback_data="seminar_info"),
# )
# admin_main.add(
#     InlineKeyboardButton("Создать рассылку", callback_data="help_spam_post"),
#     InlineKeyboardButton("Обновить промо", callback_data="admin_update_promo"),
# )
# admin_main.add(
#     InlineKeyboardButton("Музыка", callback_data="music_pre_list"),
#     InlineKeyboardButton("Добавить музыку", callback_data="music_pre_add"),
# )


def get_for_all_btn():
    return InlineKeyboardMarkup().add(InlineKeyboardButton("☑️ Выбрать", callback_data="promo_tchr" + "no"))


def get_teacher_pr(name):
    return InlineKeyboardMarkup().add(InlineKeyboardButton("☑️ Выбрать", callback_data="promo_tchr" + name))


def gen_promo_del(pr):
    return InlineKeyboardMarkup().add(InlineKeyboardButton("Удалить", callback_data="promo_delete" + pr))


def gen_teacher_delete_button(phone):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Удалить", callback_data="admin_teacher_delete_" + phone))
    return kb


def get_teacher_id_button(t_id):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("☑️ Выбрать", callback_data="teacher_id_" + t_id))
    return kb


def get_teachers_teacher_id_button(t_id):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("☑️ Выбрать ", callback_data="teachers_teacher_id" + str(t_id)))
    return kb


def gen_admin_delete_button(phone):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Удалить", callback_data="admin_delete_" + phone))
    return kb


def get_event_delete_and_edit_button(event_id):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Удалить", callback_data=f"timetable_delete_{event_id}"))
    kb.add(InlineKeyboardButton("Редактировать", callback_data=f"edit_event_{event_id}"))
    return kb


def get_event_accept_button(ev_id):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("✍️ Записаться", callback_data="payments_group_class_" + str(ev_id)))
    return kb


def get_user_phone(user_id):
    kb = InlineKeyboardMarkup()
    phone = db.get_phone_user_by_id(user_id)
    kb.row(InlineKeyboardButton(f"+7{phone}", callback_data="get_user_phone_db_" + str(phone)))
    return kb


def get_balance(abonement_count, one_time_pass_count):
    kb = InlineKeyboardMarkup()
    if abonement_count > 0:
        kb.add(
            InlineKeyboardButton('В абонементе отлаось "' + str(abonement_count) + '" занятий', callback_data="null")
        )
    if one_time_pass_count > 0:
        kb.add(
            InlineKeyboardButton('Осталось "' + str(one_time_pass_count) + '" разовых занятий', callback_data="null")
        )
    return kb


def get_pay_ways_button(can_ab, can_ot, cls_id):
    kb = InlineKeyboardMarkup()
    if can_ab != 0:
        kb.add(
            InlineKeyboardButton(
                "Оплатить абонементом (" + str(can_ab) + " занятий)", callback_data="payments_by_ab_" + cls_id
            )
        )
    if can_ot != 0:
        kb.add(
            InlineKeyboardButton(
                "Оплатить разовым занятием (" + str(can_ot) + " занятий)", callback_data="payments_by_ot_" + cls_id
            )
        )
    return kb


make_event_confirm_teacher = InlineKeyboardMarkup()
make_event_confirm_teacher.row(
    InlineKeyboardButton("Продолжить", callback_data="event_confirm_teacher_yes"),
    InlineKeyboardButton("Отмена", callback_data="event_confirm_teacher_no"),
)

make_event_confirm_admin = InlineKeyboardMarkup()
make_event_confirm_admin.row(
    InlineKeyboardButton("Продолжить", callback_data="event_confirm_admin_yes"),
    InlineKeyboardButton("Отмена", callback_data="event_confirm_admin_no"),
)

client_teachers = InlineKeyboardMarkup()
client_teachers.add(InlineKeyboardButton("Cписок учителей", callback_data="teachers_get_list"))

teachers_main_pannel = InlineKeyboardMarkup()
teachers_main_pannel.row(InlineKeyboardButton("Список занятий", callback_data="teachers_classes"))
teachers_main_pannel.row(InlineKeyboardButton("Добавить занятие", callback_data="teachers_class_add"))
teachers_main_pannel.row(InlineKeyboardButton("Изменить промо", callback_data="teachers_free_lesson"))


def gen_teacher_panel(tg_id):
    ret = copy.deepcopy(teachers_main_pannel)
    if not db.get_teacher_by_id(tg_id).get().photo:
        ret.row(InlineKeyboardButton("Добавить фото", callback_data="teachers_change_profile_photo"))
    else:
        ret.row(InlineKeyboardButton("Изменить фото", callback_data="teachers_change_profile_photo"))
    return ret


def get_teacher_pay_close_button(ev_id):
    b = InlineKeyboardMarkup()
    b.add(InlineKeyboardButton("Закрыть платеж", callback_data="admin_teacher_pay_confirm" + str(ev_id)))
    return b


def gen_class_link(url):
    b = InlineKeyboardMarkup()
    b.add(InlineKeyboardButton("Ссылка на zoom", url=url))
    return b


def delete_rescue_button(r_id):
    return InlineKeyboardMarkup().add(InlineKeyboardButton("Удалить", callback_data="help_delete" + str(r_id)))


def generate_category_keyboard(show_empty=False):
    client_store = InlineKeyboardMarkup()
    for category in db.get_all_categories():
        if show_empty or db.get_products_by_category(category):
            client_store.row(InlineKeyboardButton(category.category, callback_data=f"category_{category.id}"))
    client_store.row(InlineKeyboardButton('Закрытые сообщества', callback_data=f"ppppp_buy_pr_club"))
    return client_store


def generate_curator_keyboard():
    curator_keyboard = InlineKeyboardMarkup()
    for curator in db.get_all_curators():
        curator_keyboard.row(InlineKeyboardButton(curator.username, callback_data=f"curator_{curator.id}"))
    return curator_keyboard


private_club_client_dt = CallbackData('ffdfsffprivate_club_rate', 'rate_id')


def generate_bought_product(user_id):
    products_bought = db.get_products_bought_by_user(user_id)
    products_bought_keyboard = InlineKeyboardMarkup()
    rates = get_user_rate(user_id)
    if len(products_bought) == 0 and len(rates) == 0:
        return None

    for product in products_bought:
        products_bought_keyboard.row(InlineKeyboardButton(f"{product.name}", callback_data=f"bought_{product.id}"))

    for rate in rates:
        products_bought_keyboard.row(
            InlineKeyboardButton(rate.rate.private_club.name,
                                 callback_data=private_club_client_dt.new(rate_id=rate.rate.id)))
    return products_bought_keyboard


def generate_product_keyboard(category, back=True):
    product_store = InlineKeyboardMarkup()
    for products in db.get_products_by_category(category):
        product_store.row(InlineKeyboardButton(f"{products.name}", callback_data=f"product_{products.id}"))
    if back:
        product_store.row(InlineKeyboardButton("« Назад", callback_data="product_back"))

    return product_store


def generate_link_keyboard(product_id) -> Union[InlineKeyboardMarkup, None]:
    product = db.get_product_by_id(product_id)
    link_keyboard = InlineKeyboardMarkup()
    if product.link and product.price:
        link_keyboard.add(InlineKeyboardButton("Узнать подобнее☝", url=product.link))
        link_keyboard.add(InlineKeyboardButton("Купить 👉", callback_data=f"buy_product_{product.id}"))
    elif product.price:
        link_keyboard.add(InlineKeyboardButton("Купить 👉", callback_data=f"buy_product_{product.id}"))
    elif product.link:
        link_keyboard.add(InlineKeyboardButton("Узнать подобнее☝", url=product.link))
    link_keyboard.add(InlineKeyboardButton("« Назад", callback_data=f"buy_product_back:{product.category}"))
    return link_keyboard


def sale_gold_collection(product_id) -> Union[InlineKeyboardMarkup, None]:
    product = db.get_product_by_id(product_id)
    link_keyboard = InlineKeyboardMarkup()
    if product.link and product.price:
        link_keyboard.add(InlineKeyboardButton("Узнать подробнее", url=product.link))
        link_keyboard.add(InlineKeyboardButton("Купить", callback_data=f"sale_gold_collection_{product.id}"))
        link_keyboard.add(InlineKeyboardButton("Далее", callback_data="next"))
    elif product.price:
        link_keyboard.add(InlineKeyboardButton("Купить", callback_data=f"sale_gold_collection_{product.id}"))
        link_keyboard.add(InlineKeyboardButton("Далее", callback_data="next"))
    elif product.link:
        link_keyboard.add(InlineKeyboardButton("Узнать подробнее", url=product.link))
        link_keyboard.add(InlineKeyboardButton("Далее", callback_data="next"))
    return link_keyboard


def sale_constructor(product_id) -> Union[InlineKeyboardMarkup, None]:
    product = db.get_product_by_id(product_id)
    link_keyboard = InlineKeyboardMarkup()
    if product.link and product.price:
        link_keyboard.add(InlineKeyboardButton("Узнать подробнее", url=product.link))
        link_keyboard.add(InlineKeyboardButton("Купить", callback_data=f"sale_constructor_{product.id}"))
        link_keyboard.add(InlineKeyboardButton("Далее", callback_data="next"))
    elif product.price:
        link_keyboard.add(InlineKeyboardButton("Купить", callback_data=f"sale_constructor_{product.id}"))
        link_keyboard.add(InlineKeyboardButton("Далее", callback_data="next"))
    elif product.link:
        link_keyboard.add(InlineKeyboardButton("Узнать подробнее", url=product.link))
        link_keyboard.add(InlineKeyboardButton("Далее", callback_data="next"))
    return link_keyboard


def sale_i_want(product_id) -> Union[InlineKeyboardMarkup, None]:
    product = db.get_product_by_id(product_id)
    link_keyboard = InlineKeyboardMarkup()
    if product.link and product.price:
        link_keyboard.add(InlineKeyboardButton("Узнать подробнее", url=product.link))
        link_keyboard.add(InlineKeyboardButton("Купить", callback_data=f"sale_i_want_{product.id}"))
        link_keyboard.add(InlineKeyboardButton("Далее", callback_data="third_next"))
    elif product.price:
        link_keyboard.add(InlineKeyboardButton("Купить", callback_data=f"sale_i_want_{product.id}"))
        link_keyboard.add(InlineKeyboardButton("Далее", callback_data="next"))
    elif product.link:
        link_keyboard.add(InlineKeyboardButton("Узнать подробнее", url=product.link))
        link_keyboard.add(InlineKeyboardButton("Далее", callback_data="next"))
    return link_keyboard


def generate_letters_keyboard(product_id) -> Union[InlineKeyboardMarkup, None]:
    product = db.get_product_by_id(product_id)
    link_keyboard = InlineKeyboardMarkup()
    if product.link and product.price:
        link_keyboard.add(InlineKeyboardButton("Узнать подробнее", url=product.link))
        link_keyboard.add(InlineKeyboardButton("Купить", callback_data=f"buy_product_{product.id}"))
        link_keyboard.add(InlineKeyboardButton("Мне нужно подумать", callback_data=f"lesson_waiting"))
    elif product.price:
        link_keyboard.add(InlineKeyboardButton("Купить", callback_data=f"buy_product_{product.id}"))
        link_keyboard.add(InlineKeyboardButton("Мне нужно подумать", callback_data=f"lesson_waiting"))
    elif product.link:
        link_keyboard.add(InlineKeyboardButton("Узнать подробнее", url=product.link))
        link_keyboard.add(InlineKeyboardButton("Мне нужно подумать", callback_data=f"lesson_waiting"))
    return link_keyboard


def generate_constructor_sale_keyboard(product_id) -> Union[InlineKeyboardMarkup, None]:
    product = db.get_product_by_id(42)
    link_keyboard = InlineKeyboardMarkup()
    if product.link and product.price:
        link_keyboard.add(InlineKeyboardButton("Узнать подробнее", url=product.link))
        link_keyboard.add(InlineKeyboardButton("Купить", callback_data=f"sale_product_{product.id}"))
        link_keyboard.add(InlineKeyboardButton("Куплю в следующий раз", callback_data=f"lesson_third_want"))
    elif product.price:
        link_keyboard.add(InlineKeyboardButton("Купить", callback_data=f"sale_product_{product.id}"))
        link_keyboard.add(InlineKeyboardButton("Куплю в следующий раз", callback_data=f"lesson_third_want"))
    elif product.link:
        link_keyboard.add(InlineKeyboardButton("Узнать подробнее", url=product.link))
        link_keyboard.add(InlineKeyboardButton("Куплю в следующий раз", callback_data=f"lesson_third_want"))
    return link_keyboard


def generate_miracle_sale_keyboard(product_id) -> Union[InlineKeyboardMarkup, None]:
    product = db.get_product_by_id(34)
    link_keyboard = InlineKeyboardMarkup()
    if product.link and product.price:
        link_keyboard.add(InlineKeyboardButton("Узнать подробнее", url=product.link))
        link_keyboard.add(InlineKeyboardButton("Купить", callback_data=f"sale_miracle_product_{product.id}"))
        link_keyboard.add(InlineKeyboardButton("Далее", callback_data="next"))
    elif product.price:
        link_keyboard.add(InlineKeyboardButton("Купить", callback_data=f"sale_miracle_product_{product.id}"))
        link_keyboard.add(InlineKeyboardButton("Далее", callback_data="next"))
    elif product.link:
        link_keyboard.add(InlineKeyboardButton("Узнать подробнее", url=product.link))
        link_keyboard.add(InlineKeyboardButton("Далее", callback_data="next"))
    return link_keyboard


def generate_edit_product():
    edit_product = InlineKeyboardMarkup()
    edit_product.row(
        InlineKeyboardButton("✏️ Название", callback_data="name"),
        InlineKeyboardButton("🏷 Категория", callback_data="category"),
    )
    edit_product.row(
        InlineKeyboardButton("📝 Описание", callback_data="description"),
        InlineKeyboardButton("🗄 Содержание", callback_data="content"),
    )
    edit_product.row(
        InlineKeyboardButton("📸 Изображение", callback_data="image"),
        InlineKeyboardButton("↗️ Ссылка", callback_data="link"),
    )
    edit_product.row(
        InlineKeyboardButton("💰 Цена", callback_data="price"),
        InlineKeyboardButton("💸 Цена со скидкой", callback_data="price_discount"),
    )
    edit_product.row(InlineKeyboardButton("💻 Уроки", callback_data="lessons"), )
    return edit_product


def generate_product_lessons(product_id):
    product_lessons = db.get_all_product_lessons_for_product(product_id)
    lesson_keyboard = InlineKeyboardMarkup()
    for product_lesson in product_lessons:
        lesson_keyboard.row(InlineKeyboardButton(f"{product_lesson.order}", callback_data=f"{product_lesson.lesson}"))
    return lesson_keyboard


def generate_edit_lessons():
    edit_lesson = InlineKeyboardMarkup()
    edit_lesson.row(
        InlineKeyboardButton("Контент", callback_data="content"), InlineKeyboardButton("Фото", callback_data="photo"),
    )
    edit_lesson.row(
        InlineKeyboardButton("Анимация", callback_data="gif"),
        InlineKeyboardButton("Документ", callback_data="document"),
    )
    return edit_lesson


def generate_product_add_lessons_keyboard(product_id):
    product_lesson = InlineKeyboardMarkup()
    product_lesson.row(
        InlineKeyboardButton("Добавить уроки", callback_data=f"lessons_add_for_product_{product_id}"),
        InlineKeyboardButton("Пропустить", callback_data=f"lessons_skip_for_product_{product_id}"),
    )
    return product_lesson


new_product_and_admin_panel_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("➕ Добавить товар", callback_data="admin_add_product")],
        [InlineKeyboardButton("🔧 Панель администратора", callback_data="admin_main")],
    ]
)

client_store_classes = InlineKeyboardMarkup()
client_store_classes.row(
    InlineKeyboardButton("🎫 Разовое занятие", callback_data="gn1"),
    InlineKeyboardButton("💎 Абонемент", callback_data="botshop_buy_aboniment"),
)

client_music = InlineKeyboardMarkup()
client_music.add(InlineKeyboardButton("🧘‍♂️ Для йоги", callback_data="music_foryoga"))
client_music.add(InlineKeyboardButton("🙏 Для медитации", callback_data="music_meditaion"))
client_music.add(InlineKeyboardButton("😴 Для шавасаны", callback_data="music_shavasana"))

freeze_confirm = InlineKeyboardMarkup()
freeze_confirm.add(InlineKeyboardButton("Подтвердить заморозку", callback_data="help_freeze_confirm"))


def gen_pay_video(lsn, b):
    if not b:
        return InlineKeyboardMarkup().add(
            InlineKeyboardButton("Купить полный видеоурок", callback_data="botshop_video_lesson" + str(lsn))
        )
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton("Смотреть полный видеоурок", callback_data="videos_show" + str(lsn))
    )


jobs_kb_data = CallbackData("jobs_data", "job_id")


def generate_jobs_kb(jobs_id: List):
    jobs_kb = InlineKeyboardMarkup()
    for job_id in jobs_id:
        job = scheduler.get_job(job_id=job_id)
        job_time = f"{job.next_run_time.hour}:{job.next_run_time.minute}"
        jobs_kb.row(InlineKeyboardButton(job_time, callback_data=jobs_kb_data.new(job_id=job_id)))
    jobs_kb.row(InlineKeyboardButton("« Назад", callback_data=jobs_kb_data.new(job_id="back")))
    return jobs_kb


manage_job_data = CallbackData("manage_job", "job_id", "prefix")


def generate_manage_job_keyboard(job_id):
    manage_job_id = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("Удалить", callback_data=manage_job_data.new(job_id=job_id, prefix="delete"))],
            [InlineKeyboardButton("« Назад", callback_data=manage_job_data.new(job_id=job_id, prefix="back"))],
        ]
    )
    return manage_job_id


accept_delete_job_data = CallbackData("accepting_delete_job", "prefix", "job_id")


def generate_accept_delete(job_id):
    accept_delete_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("Да", callback_data=accept_delete_job_data.new(prefix="yes", job_id=job_id))],
            [InlineKeyboardButton("Нет", callback_data=accept_delete_job_data.new(prefix="no", job_id=job_id))],
        ]
    )
    return accept_delete_kb


def gen_pay_course(lsn, b, num=1, ty="v"):
    if not b:
        return InlineKeyboardMarkup().add(
            InlineKeyboardButton("💳 купить курс ", callback_data="botshop_course" + str(lsn))
        )
    if num == 0:
        return InlineKeyboardMarkup().add(
            InlineKeyboardButton("Полный видеокурс", callback_data="course_show" + str(lsn) + ":1:v")
        )
    if ty == "v":
        return InlineKeyboardMarkup().add(
            InlineKeyboardButton("Тест по видео", callback_data="course_show" + str(lsn) + ":" + str(num) + ":" + "q")
        )
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton("Следующий урок", callback_data="course_show" + str(lsn) + ":" + str(num) + ":" + ty)
    )


admin_edit_product_course = InlineKeyboardMarkup()
admin_edit_product_course.row(InlineKeyboardButton("Добавить новый курс", callback_data=f"add_new_curator_course"))
admin_edit_product_course.row(InlineKeyboardButton("Удалить курс", callback_data=f"delete_curator_course"))

back_keyboard = InlineKeyboardMarkup()
back_keyboard.row(InlineKeyboardButton("« Назад", callback_data="admin_section_curator"))
