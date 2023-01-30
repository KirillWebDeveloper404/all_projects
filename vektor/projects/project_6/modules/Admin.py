import logging
from datetime import date

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import ChatNotFound

import modules.Config as Cfg
from loader import bot, dp
from modules import Methods
from modules.BotKeyboards import new_product_and_admin_panel_kb
from modules.Mailing import MailingStates
from modules.Methods import is_url_valid


class Num(StatesGroup):
    waiting_for_number = State()


class RegisterTeacher(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()


class AddCategory(StatesGroup):
    waiting_for_category = State()


class RemoveCategory(StatesGroup):
    waiting_for_category = State()


class AddVideo(StatesGroup):
    waiting_for_name = State()
    waiting_for_video = State()


class AddGif(StatesGroup):
    waiting_for_name = State()
    waiting_for_animation = State()


class AddPhoto(StatesGroup):
    waiting_for_name = State()
    waiting_for_photo = State()


# класс состояний для добавления продукта
class AddProduct(StatesGroup):
    waiting_for_category = State()
    waiting_for_name = State()
    waiting_for_description = State()
    waiting_for_price = State()
    waiting_for_discount_price = State()
    waiting_for_image = State()
    waiting_for_link = State()
    waiting_for_content = State()


class AddCurator(StatesGroup):
    waiting_for_username = State()
    waiting_for_product = State()


class DelCurator(StatesGroup):
    init = State()


class EditCurator(StatesGroup):
    init = State()
    waiting_for_field = State()
    waiting_for_name_value = State()
    waiting_for_phone_value = State()
    waiting_for_course_edit = State()
    waiting_for_course_delete = State()
    waiting_for_add_course = State()


class AddLesson(StatesGroup):
    init = State()
    waiting_for_photo = State()
    waiting_for_gif = State()
    waiting_for_document = State()
    waiting_for_content = State()


class RemoveProduct(StatesGroup):
    waiting_for_category = State()
    waiting_for_product = State()


class EditProduct(StatesGroup):
    waiting_for_category = State()
    waiting_for_product = State()
    waiting_for_column = State()
    waiting_for_new_value = State()


class EditLesson(StatesGroup):
    waiting_for_lesson = State()
    waiting_for_column = State()
    waiting_for_new_value = State()


class AddEventDialog(StatesGroup):
    waiting_for_event_date = State()
    waiting_for_event_start_time = State()
    waiting_for_event_duration = State()
    waiting_for_event_teacher = State()
    waiting_for_event_description = State()
    waiting_for_event_url = State()
    waiting_for_event_confirm = State()


class EditEventDialog(StatesGroup):
    date = State()
    time_start = State()
    time_end = State()
    teacher = State()
    description = State()
    url = State()
    confirm = State()


# диалог создания нового события в календаре
@dp.callback_query_handler(
    (lambda c: c.data and c.data.startswith("choose_date")), state=AddEventDialog.waiting_for_event_date
)
async def add_event_date(callback: types.CallbackQuery, state: FSMContext):
    dt = callback.data.split("choose_date")[1]
    dt = Methods.validate_date_or_none(dt)
    await state.update_data(date=dt)
    await bot.send_message(
        callback.from_user.id,
        "Введите время начала события в формате *часы:минуты*",
        parse_mode=types.ParseMode.MARKDOWN,
    )
    await AddEventDialog.waiting_for_event_start_time.set()


@dp.message_handler(state=AddEventDialog.waiting_for_event_start_time, content_types=types.ContentType.TEXT)
async def get_event_time(message: types.Message, state: FSMContext):
    t = Methods.validate_time_or_none(message.text)
    if not t:
        await bot.send_message(message.from_user.id, "Неверный формат времени! Введите заново")
        await AddEventDialog.waiting_for_event_start_time.set()
        return
    await state.update_data(time_start=t)
    await bot.send_message(
        message.from_user.id,
        "Введите время длительности события в формате *часы:минуты*",
        parse_mode=types.ParseMode.MARKDOWN,
    )

    await AddEventDialog.waiting_for_event_duration.set()


@dp.message_handler(state=AddEventDialog.waiting_for_event_duration, content_types=types.ContentType.TEXT)
async def get_event_duration(message: types.Message, state: FSMContext):
    t = Methods.validate_time_or_none(message.text)
    if not t:
        await bot.send_message(message.from_user.id, "Неверный формат времени! Введите заново")
        await AddEventDialog.waiting_for_event_duration.set()
        return
    start = await state.get_data()
    start = start["time_start"]
    t = Methods.add_two_times(t, start)
    await state.update_data(time_end=t)
    await bot.send_message(message.from_user.id, "Выберите учителя")
    for t in db.get_teachers():
        if t.tg_id:
            await bot.send_message(
                message.from_user.id, t.name + "\n" + t.phone_number, reply_markup=kb.get_teacher_id_button(t.tg_id)
            )
    await AddEventDialog.waiting_for_event_teacher.set()


@dp.callback_query_handler(
    (lambda c: c.data and c.data.startswith("teacher_id")), state=AddEventDialog.waiting_for_event_teacher
)
async def add_event_get_teacher(callback: types.CallbackQuery, state: FSMContext):
    command = callback.data.split("teacher_id_")[1]
    await state.update_data(tg_id=command)
    await bot.send_message(
        callback.from_user.id,
        "Вы выбрали учителя:\n"
        + db.get_teacher_by_id(command).get().name
        + "\nВведите описание события (может быть пустым, тогда введите 'Пропустить')",
    )
    await AddEventDialog.waiting_for_event_description.set()


@dp.message_handler(state=AddEventDialog.waiting_for_event_description, content_types=types.ContentType.TEXT)
async def get_event_descr(message: types.Message, state: FSMContext):
    d = message.text
    if d == "Пропустить":
        d = ""
    await state.update_data(description=d)
    await bot.send_message(
        message.from_user.id, "Введите ссылку на zoom конференцию",
    )
    await AddEventDialog.waiting_for_event_url.set()


@dp.message_handler(state=AddEventDialog.waiting_for_event_url, content_types=types.ContentType.TEXT)
async def get_event_get_url(message: types.Message, state: FSMContext):
    if not is_url_valid(message.text):
        await message.reply("Пожалуйста, введите правильную ссылку. Например: https://us04web.zoom.us/j/123?pwd=456")
        return
    await state.update_data(url=message.text)
    dt = await state.get_data()
    await bot.send_message(
        message.from_user.id,
        f"Событие\n"
        f"Дата: {dt['date']}\n"
        f"Время начала: {dt['time_start']}\n"
        f"Время окончания: {dt['time_end']}\n"
        f"Проводящий учитель: {db.get_teacher_by_id(dt['tg_id']).get().name}\n"
        f"Описание: {dt['description']}\n"
        f"Ссылка: {dt['url']}",
        reply_markup=kb.make_event_confirm_admin,
    )
    await AddEventDialog.waiting_for_event_confirm.set()


@dp.callback_query_handler(
    (lambda c: c.data and c.data.startswith("event_confirm_admin")), state=AddEventDialog.waiting_for_event_confirm
)
async def add_event_get_teacher(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "event_confirm_admin_yes":
        d = await state.get_data()
        db.add_new_event(
            event_start=d["time_start"],
            event_end=d["time_end"],
            descr=d["description"],
            date=d["date"],
            teacher_id=d["tg_id"],
            url=d["url"],
        )
        await state.finish()
        await bot.send_message(
            callback_query.from_user.id, "Событие успешно создано",
        )
    else:
        await state.finish()
        await bot.send_message(
            callback_query.from_user.id, "Создание события отменено",
        )


# edit event dialogue
@dp.callback_query_handler(lambda c: c.data and c.data.startswith("edit_event"))
async def edit_event(callback: types.CallbackQuery, state: FSMContext):
    event_id = callback.data.split("edit_event_")[1]
    logging.debug(f"entered edit event dialogue")
    await state.update_data(event_id=event_id)
    await bot.send_message(
        callback.from_user.id,
        "Отправьте новую дату занятия в формате *год.месяц.день*\nИли отправьте команду /skip, чтобы пропустить",
        parse_mode=types.ParseMode.MARKDOWN,
    )
    await EditEventDialog.date.set()


@dp.message_handler(state=EditEventDialog.date, content_types=types.ContentType.TEXT)
async def edit_event_date(message: types.Message, state: FSMContext):
    logging.debug(f"entered event's date editing")
    if "skip" not in message.text:
        logging.debug("setting up new date")
        validated_date = Methods.validate_date_or_none(message.text)
        if not validated_date:
            await bot.send_message(
                message.from_user.id,
                "Введите дату заново, неверный формат *год.месяц.день*",
                parse_mode=types.ParseMode.MARKDOWN,
            )
            return
        await state.update_data(date=validated_date, notify_users=True)

    await bot.send_message(
        message.from_user.id,
        "Отправьте новое время начала в формате *часы:минуты*\nИли отправьте команду /skip, чтобы пропустить",
        parse_mode=types.ParseMode.MARKDOWN,
    )
    await EditEventDialog.time_start.set()


@dp.message_handler(state=EditEventDialog.time_start, content_types=types.ContentType.TEXT)
async def edit_event_time_start(message: types.Message, state: FSMContext):
    logging.debug(f"entered event's start time editing")
    if "skip" not in message.text:
        logging.debug("setting up new start time")
        t = Methods.validate_time_or_none(message.text)
        if not t:
            await bot.send_message(message.from_user.id, "Неверный формат времени! Введите заново")
            return
        await state.update_data(time_start=t, notify_users=True)

    await bot.send_message(
        message.from_user.id,
        "Отправьте новую длительность события в формате *часы:минуты*\n"
        "Или отправьте команду /skip, чтобы пропустить",
        parse_mode=types.ParseMode.MARKDOWN,
    )
    await EditEventDialog.time_end.set()


@dp.message_handler(state=EditEventDialog.time_end, content_types=types.ContentType.TEXT)
async def edit_event_time_end(message: types.Message, state: FSMContext):
    logging.debug(f"entered event's time_end editing")
    if "skip" not in message.text:
        logging.debug("setting up new time_end")
        t = Methods.validate_time_or_none(message.text)
        if not t:
            await bot.send_message(message.from_user.id, "Неверный формат времени! Введите заново")
            return
        data = await state.get_data()
        if "time_start" in data:
            start = data["time_start"]
        else:
            start = db.get_event_by_id(data["event_id"]).event_time_start
        t = Methods.add_two_times(t, start)
        await state.update_data(time_end=t, notify_users=True)

    await bot.send_message(message.from_user.id, "Выберите учителя")
    for t in db.get_teachers():
        if t.tg_id:
            await bot.send_message(
                message.from_user.id, t.name + "\n" + t.phone_number, reply_markup=kb.get_teacher_id_button(t.tg_id)
            )
    await EditEventDialog.teacher.set()


@dp.callback_query_handler((lambda c: c.data and c.data.startswith("teacher_id")), state=EditEventDialog.teacher)
async def edit_event_teacher(callback: types.CallbackQuery, state: FSMContext):
    command = callback.data.split("teacher_id_")[1]
    await state.update_data(tg_id=command)
    await bot.send_message(
        callback.from_user.id,
        f"Вы выбрали учителя: {db.get_teacher_by_id(command).get().name}\n"
        "Введите описание события\n"
        "Или отправьте команду /skip, чтобы пропустить",
    )
    await EditEventDialog.description.set()


@dp.message_handler(state=EditEventDialog.description, content_types=types.ContentType.TEXT)
async def edit_event_description(message: types.Message, state: FSMContext):
    logging.debug(f"entered event's description editing")
    if "skip" not in message.text:
        logging.debug("setting up new description")
        await state.update_data(description=message.text, notify_users=True)

    await bot.send_message(
        message.from_user.id,
        "Введите ссылку на zoom конференцию\nИли отправьте команду /skip, чтобы пропустить",
        parse_mode=types.ParseMode.MARKDOWN,
    )
    await EditEventDialog.url.set()


@dp.message_handler(state=EditEventDialog.url, content_types=types.ContentType.TEXT)
async def edit_event_url(message: types.Message, state: FSMContext):
    logging.debug(f"entered event's url editing")
    if "skip" not in message.text:
        logging.debug("setting up new url")
        if not is_url_valid(message.text):
            await message.reply(
                "Пожалуйста, введите правильную ссылку. Например: https://us04web.zoom.us/j/123?pwd=456"
            )
            return
        await state.update_data(url=message.text)

    dt = await state.get_data()
    updating_message = "\n".join([f"{k}: {v}" for k, v in dt.items()])
    await bot.send_message(
        message.from_user.id, f"Обновляется:\n{updating_message}", reply_markup=kb.make_event_confirm_admin,
    )
    await EditEventDialog.confirm.set()


@dp.callback_query_handler(
    (lambda c: c.data and c.data.startswith("event_confirm_admin")), state=EditEventDialog.confirm
)
async def edit_event_confirm(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "event_confirm_admin_yes":
        data = await state.get_data()
        notify_users = data.get("notify_users", False)
        event_id = data["event_id"]
        db.update_event(data)
        db.update_links_for_event(data)
        updated_event = db.get_event_by_id(event_id)

        # if a notification is required, notify users that an event is edited
        users_attending_event = db.get_users_by_event_id(event_id)
        if notify_users and users_attending_event:
            for user in users_attending_event:
                logging.debug(f"sending a notification to {user.tg_id}")
                try:
                    await bot.send_message(
                        user.tg_id,
                        f"Привет!\n"
                        f"В событии, на которое ты записан, произошли изменения\n"
                        f"Актуальная информация\n"
                        f"Преподаватель: *{updated_event.teacher_name}*\n"
                        f"Дата проведения: *{updated_event.event_date}*\n"
                        f"Время начала: *{updated_event.event_time_start}*\n"
                        f"Время окончания: *{updated_event.event_time_end}*\n"
                        f"{updated_event.description}",
                        parse_mode=types.ParseMode.MARKDOWN,
                    )
                except ChatNotFound:
                    logging.warning(f"impossible to notify {user.tg_id}")
            await bot.send_message(
                callback_query.from_user.id,
                f"Оповещение отправлено: {', '.join([u.name for u in users_attending_event])}",
            )
        await state.finish()
        await bot.send_message(
            callback_query.from_user.id, "Редактирование события прошло успешно",
        )
    else:
        await state.finish()
        await bot.send_message(
            callback_query.from_user.id, "Редактирование события отмененео",
        )


@dp.callback_query_handler(lambda c: c.data and c.data.startswith("promo"))
async def process_admin_callback(cb: types.CallbackQuery):
    """
    обработчик функций для создания промокода
    """
    cmd = cb.data.split("promo_")[1]
    if cmd == "add":
        logging.info("adding promo by admin: " + str(cb.from_user.id))
        await bot.send_message(
            cb.from_user.id, "Выберите учителя",
        )
        for t in db.get_teachers():
            if t.tg_id:
                await bot.send_message(
                    cb.from_user.id, t.name + "\n" + t.phone_number, reply_markup=kb.get_teacher_pr(t.name)
                )
        await bot.send_message(cb.from_user.id, "Для всех", reply_markup=kb.get_for_all_btn())
    elif "tchr" in cmd:
        cmd = cmd.split("tchr")[1]
        if cmd == "no":
            p = db.create_promo(None)
        else:
            p = db.create_promo(cmd)
        await bot.send_message(
            cb.from_user.id, f"Промокод {p} успешно создан",
        )
        return
    elif cmd == "list":
        for p in db.get_promos():
            await bot.send_message(cb.from_user.id, p.promo, reply_markup=kb.gen_promo_del(p.promo))
        return
    elif "delete" in cmd:
        cmd = cmd.split("delete")[1]
        db.find_promo(cmd).get().delete_instance()
        await bot.send_message(
            cb.from_user.id, "Промокод успешно удален",
        )
        return


class SetPromo(StatesGroup):
    video = State()


# обработчик для добавления учителю промо видео
@dp.message_handler(state=SetPromo.video, content_types=["video"])
async def set_video(m, state):
    t_id = await state.get_data()
    t_id = t_id["t_id"]
    db.set_teacher_video(t_id, m.video.file_id)
    await bot.send_message(
        m.from_user.id, "Видео успешно загружено",
    )
    await state.finish()


@dp.callback_query_handler(lambda c: c.data and c.data.startswith("admin_"), state="*")
async def process_admin_callback(cllbckquery: types.CallbackQuery, state: FSMContext):
    """
    обработчик клавиш панели администратора
    """
    command = cllbckquery.data.split("admin_")[1]
    if command == "main":
        await cllbckquery.answer()
        await cllbckquery.message.edit_text(Cfg.ADMIN_MSG)
        await cllbckquery.message.edit_reply_markup(reply_markup=kb.admin_main)
    elif "section_shop" in command:
        await bot.edit_message_reply_markup(
            cllbckquery.from_user.id, cllbckquery.message.message_id, reply_markup=kb.admin_shop
        )
    elif "section_curator" in command:
        await cllbckquery.message.edit_text("Управление кураторами", reply_markup=kb.curator_changes)

    elif "section_video" in command:
        await bot.edit_message_reply_markup(
            cllbckquery.from_user.id, cllbckquery.message.message_id, reply_markup=kb.admin_video
        )
    elif "add_video" in command:
        await bot.send_message(cllbckquery.from_user.id, "Введите название видео")
        await AddVideo.waiting_for_name.set()
    elif "main_curator_list" in command:

        text = "Список кураторов:\n\n"
        for curator in db.get_all_curators():
            text += f"Куратор {curator.username}\nТелефон: {curator.phone_number}\n"
        await bot.send_message(cllbckquery.from_user.id, text)
    elif "main_curator_add" in command:
        await bot.send_message(cllbckquery.from_user.id, "Отправьте никнейм нового куратора")
        await AddCurator.waiting_for_username.set()
    elif "main_curator_delete" in command:
        await bot.send_message(
            cllbckquery.from_user.id,
            "Выберите куратора, которого требуется удалить",
            reply_markup=kb.generate_curator_keyboard(),
        )
        await DelCurator.init.set()
    elif "main_curator_edit" in command:
        await bot.send_message(
            cllbckquery.from_user.id,
            "Выберите куратора, чьи данные хотите изменить",
            reply_markup=kb.generate_curator_keyboard(),
        )
        await EditCurator.init.set()
    # elif "delete_video" in command:
    # todo delete video by name in kb.generate_video_keyboard
    elif "add_gif" in command:
        await bot.send_message(cllbckquery.from_user.id, "Введите название анимации")
        await AddGif.waiting_for_name.set()

    elif "add_photo" in command:
        await bot.send_message(cllbckquery.from_user.id, "Введите название изображения")
        await AddPhoto.waiting_for_name.set()

    elif "add_category" in command:
        await bot.send_message(cllbckquery.from_user.id, "Введите название новой категории")
        await AddCategory.waiting_for_category.set()

    elif "delete_category" in command:
        await bot.send_message(
            cllbckquery.from_user.id,
            "Введите название категории, которую требуется удалить",
            reply_markup=kb.generate_category_keyboard(show_empty=True),
        )
        await RemoveCategory.waiting_for_category.set()

    elif "add_product" in command:
        await bot.send_message(
            cllbckquery.from_user.id,
            "Выберите категорию продукта",
            reply_markup=kb.generate_category_keyboard(show_empty=True),
        )
        await AddProduct.waiting_for_category.set()

    elif "delete_product" in command:
        await bot.send_message(
            cllbckquery.from_user.id,
            "Выберите категорию продукта",
            reply_markup=kb.generate_category_keyboard(show_empty=True),
        )
        await RemoveProduct.waiting_for_category.set()

    elif "edit_product" in command:
        await bot.send_message(
            cllbckquery.from_user.id,
            "Выберите категорию изменяемого продукта",
            reply_markup=kb.generate_category_keyboard(show_empty=False),
        )
        await EditProduct.waiting_for_category.set()

    elif "update_promo" in command:
        # выводит список для обновления промо видео
        await bot.send_message(
            cllbckquery.from_user.id, "Выберите учителя",
        )
        for i in db.get_teachers():
            if i.tg_id:
                await bot.send_message(
                    cllbckquery.from_user.id,
                    i.name,
                    reply_markup=types.InlineKeyboardMarkup().add(
                        types.InlineKeyboardButton("Обновить видео", callback_data="admin_upd_video" + str(i.tg_id))
                    ),
                )
    elif "upd_video" in command:
        # обновляет промо видео
        id = int(command.split("upd_video")[1])
        await state.update_data(t_id=id)
        await bot.send_message(
            cllbckquery.from_user.id, "Отправьте новое видео",
        )
        await SetPromo.video.set()
    elif "teacher_pay_confirm" in command:
        # помечает, что класс был оплачен учителем
        i = command.split("teacher_pay_confirm")[1]
        db.set_event_payed(int(i))
        await bot.send_message(
            cllbckquery.from_user.id, "Платеж помечен как закрытый",
        )
        return
    elif command == "add":
        # запускает процесс добавления админа
        await bot.send_message(cllbckquery.from_user.id, Cfg.ADD_ADMIN)
        await Num.waiting_for_number.set()
        logging.info("Adding admin started")
        return
    elif command == "add_teacher":
        # запускает процесс добавления учителя
        await bot.send_message(cllbckquery.from_user.id, "Введите имя учителя")
        await RegisterTeacher.waiting_for_name.set()
        logging.info("Adding teacher started, admin: " + str(cllbckquery.from_user.id))
        return
    elif command == "list":
        for admin in db.get_admins():
            if admin.tg_id is None:
                await bot.send_message(
                    cllbckquery.from_user.id,
                    "Администратор по номеру: +7" + admin.phone_number + " еще не подтвердил свой аккаунт.",
                    reply_markup=kb.gen_admin_delete_button(admin.phone_number),
                )
            elif admin.tg_id == str(cllbckquery.from_user.id):
                continue
            else:
                await bot.send_message(
                    cllbckquery.from_user.id,
                    "имя: " + admin.name + "\nномер: " + admin.phone_number,
                    reply_markup=kb.gen_admin_delete_button(admin.phone_number),
                )
    elif "list_teacher" in command:
        # выводит список учителей
        for t in db.get_teachers():
            if t.tg_id is None:
                await bot.send_message(
                    cllbckquery.from_user.id,
                    "имя: " + t.name + "\nномер: " + t.phone_number + "\nНомер не подтвержден",
                    reply_markup=kb.gen_teacher_delete_button(t.phone_number),
                )
            elif t.tg_id == cllbckquery.from_user.id:
                continue
            else:
                await bot.send_message(
                    cllbckquery.from_user.id,
                    "имя: " + t.name + "\nномер: " + t.phone_number,
                    reply_markup=kb.gen_teacher_delete_button(t.phone_number),
                )
        return
    elif "add_event" in command:
        # запускает процесс добавления занятия
        await bot.send_message(
            cllbckquery.from_user.id,
            "Выберите дату занятия ",
            parse_mode=types.ParseMode.MARKDOWN,
            reply_markup=kb.gen_month_date_chose(str(cllbckquery.message.message_id + 1), date.today()),
        )
        await AddEventDialog.waiting_for_event_date.set()
        logging.info("Adding event started by: " + str(cllbckquery.from_user.id))
        return
    elif "list_event" in command:
        # выводит календарь админа
        await bot.send_message(
            cllbckquery.from_user.id,
            "Выберите день",
            reply_markup=kb.gen_month_for_admin(str(cllbckquery.message.message_id + 1), date.today()),
        )
    elif "teacher_delete" in command:
        # удаляет учителя
        command = command.split("teacher_delete_")[1]
        db.rm_teacher_by_phone(command)
        await bot.send_message(cllbckquery.from_user.id, "Учитель успешно удален", reply_markup=kb.admin_main)
        logging.info("teacher deleted id: " + command + " by admin: " + str(cllbckquery.from_user.id))
        return
    elif "delete_" in command:
        # удаляет админа
        command = command.split("delete_")[1]
        db.rm_admin_by_phone(command)
        await bot.send_message(cllbckquery.from_user.id, "Админ успешно удален", reply_markup=kb.admin_main)
        logging.info("admin deleted id: " + command + "by admin: " + str(cllbckquery.from_user.id))


@dp.message_handler(state=AddCategory.waiting_for_category, content_types=types.ContentType.TEXT)
async def add_category(message: types.Message):
    category = message.text
    db.create_category(category)
    await bot.send_message(message.from_user.id, f"Категория '{category}' добавлена")


@dp.callback_query_handler(
    lambda c: c.data and c.data.startswith("category_"), state=RemoveCategory.waiting_for_category
)
async def deleted_category(callback: types.CallbackQuery, state: FSMContext):
    category_id = callback.data.split("category_")[1]
    db.rm_category_by_id(category_id)
    await bot.send_message(callback.from_user.id, f"Категория и товары из этой категории успешно удалены")


@dp.message_handler(state=AddCurator.waiting_for_username, content_types=types.ContentType.TEXT)
async def get_curator_phone(message: types.Message, state: FSMContext):
    username = message.text
    curator = db.save_curator(username=username)
    await state.update_data(username=username)
    await state.update_data(curator_id=curator.id)
    await bot.send_message(
        message.from_user.id,
        f"Куратор {curator.username} сохранен. Далее выберите курс или "
        f"продукт, за который куратор будет ответственен.",
        reply_markup=kb.not_deleted_products,
    )
    await AddCurator.waiting_for_product.set()


@dp.callback_query_handler(
    lambda c: c.data and c.data.startswith("not_deleted_product_curator_"), state=AddCurator.waiting_for_product
)
async def select_product_curator(callback: types.CallbackQuery, state: FSMContext):
    product_id = callback.data.split("not_deleted_product_curator_")[1]
    product = db.get_product_by_id(product_id)
    data = await state.get_data()
    db.save_product_curator(product_id, data["curator_id"])
    username = data["username"]

    db.fill_curators_shoplist(product_id)

    await bot.send_message(
        callback.from_user.id,
        f"Куратор {username} успешно добавлен и ответственен за {product.name}",
        reply_markup=kb.back_keyboard,
    )
    await state.finish()


@dp.callback_query_handler(lambda c: c.data and c.data.startswith("curator_"), state=EditCurator.init)
async def edit_curator_init(callback: types.CallbackQuery, state: FSMContext):
    curator_id = callback.data.split("curator_")[1]
    # curator = db.get_curator_by_id(curator_id)
    curator_keyboard = InlineKeyboardMarkup()
    curator_keyboard.row(InlineKeyboardButton("Имя куратора", callback_data=f"name_curator_{curator_id}"))
    curator_keyboard.row(InlineKeyboardButton("Телефонный номер", callback_data=f"phone_curator_{curator_id}"))
    curator_keyboard.row(InlineKeyboardButton("Курируемые курсы", callback_data=f"courses_curator_{curator_id}"))
    await bot.send_message(callback.from_user.id, "Какое поле вы хотите измениь?", reply_markup=curator_keyboard)
    await EditCurator.waiting_for_field.set()


@dp.callback_query_handler(
    lambda c: c.data and c.data.startswith("courses_curator_"), state=EditCurator.waiting_for_field
)
async def edit_curator_name(callback: types.CallbackQuery, state: FSMContext):
    curator_id = callback.data.split("courses_curator_")[1]

    await state.update_data(curator_id=curator_id)
    await bot.send_message(callback.from_user.id, "Что требуется сделать?", reply_markup=kb.admin_edit_product_course)
    await EditCurator.waiting_for_course_edit.set()


@dp.callback_query_handler(
    lambda c: c.data and c.data.startswith("add_new_curator_course"), state=EditCurator.waiting_for_course_edit
)
async def add_new_course(callback: types.CallbackQuery, state: FSMContext):
    await bot.send_message(
        callback.from_user.id, "Выберите какой курс требуется добавить", reply_markup=kb.not_deleted_products
    )
    await EditCurator.waiting_for_add_course.set()


@dp.callback_query_handler(
    lambda c: c.data and c.data.startswith("not_deleted_product_curator_"), state=EditCurator.waiting_for_add_course
)
async def select_product_curator(callback: types.CallbackQuery, state: FSMContext):
    product_id = callback.data.split("not_deleted_product_curator_")[1]
    product = db.get_product_by_id(product_id)
    data = await state.get_data()
    curator = db.get_curator_by_id(data["curator_id"])
    user = db.get_user_by_tg_id(callback.from_user.id)

    if db.is_product_lead_by_curator(product_id, data["curator_id"]):
        keyboard = InlineKeyboardMarkup()
        keyboard.row(InlineKeyboardButton("« Назад к выбору курса", callback_data="add_new_curator_course"))
        await bot.send_message(
            callback.from_user.id,
            f"Куратор {curator.username} уже ведет выбранный курс, выберите " f"другой",
            reply_markup=keyboard,
        )
        await EditCurator.waiting_for_course_edit.set()
    else:
        db.save_product_curator(product_id, data["curator_id"])
        db.update_curator_shoplist(user.id, product_id, data["curator_id"])
        await bot.send_message(
            callback.from_user.id,
            f"Куратор {curator.username} успешно изменен и ответственен также за {product.name}",
            reply_markup=kb.back_keyboard,
        )
        await state.finish()


@dp.callback_query_handler(
    lambda c: c.data and c.data.startswith("delete_curator_course"), state=EditCurator.waiting_for_course_edit
)
async def delete_course(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    curator_id = data["curator_id"]
    if db.get_products_by_curator(curator_id):
        await bot.send_message(
            callback.from_user.id,
            "Выберите какой курс требуется удалить",
            reply_markup=kb.generate_product_by_curator(curator_id),
        )
        await EditCurator.waiting_for_course_delete.set()
    else:
        await bot.send_message(
            callback.from_user.id, "Куратор еще не ведет курсов", reply_markup=kb.back_keyboard,
        )


@dp.callback_query_handler(
    lambda c: c.data and c.data.startswith("rm_product_by_curator_"), state=EditCurator.waiting_for_course_delete
)
async def final_delete_course(callback: types.CallbackQuery, state: FSMContext):
    product_id = callback.data.split("rm_product_by_curator_")[1]
    product = db.get_product_by_id(product_id)
    data = await state.get_data()
    curator_id = data["curator_id"]
    db.rm_product_curator(product_id, curator_id)
    await bot.send_message(
        callback.from_user.id, f"Куратор больше не ведет курс {product.name}", reply_markup=kb.back_keyboard
    )
    await state.finish()


@dp.callback_query_handler(lambda c: c.data and c.data.startswith("name_curator_"), state=EditCurator.waiting_for_field)
async def edit_curator_name(callback: types.CallbackQuery, state: FSMContext):
    curator_id = callback.data.split("name_curator_")[1]
    await state.update_data(curator_id=curator_id)
    await bot.send_message(callback.from_user.id, "Введите новое имя куратора")
    await EditCurator.waiting_for_name_value.set()


@dp.message_handler(state=EditCurator.waiting_for_name_value, content_types=types.ContentType.TEXT)
async def process_edit_curator_value(message: types.Message, state: FSMContext):
    data = await state.get_data()
    new_name = message.text
    db.edit_curator(data["curator_id"], new_name)
    await bot.send_message(message.from_user.id, "Имя куратора успешно изменено")
    await state.finish()


@dp.callback_query_handler(
    lambda c: c.data and c.data.startswith("phone_curator_"), state=EditCurator.waiting_for_field
)
async def edit_curator_phone(callback: types.CallbackQuery, state: FSMContext):
    curator_id = callback.data.split("phone_curator_")[1]
    await state.update_data(curator_id=curator_id)
    await bot.send_message(callback.from_user.id, "Введите новый телефон куратора")
    await EditCurator.waiting_for_phone_value.set()


@dp.message_handler(state=EditCurator.waiting_for_phone_value, content_types=types.ContentType.TEXT)
async def process_edit_curator_value(message: types.Message, state: FSMContext):
    data = await state.get_data()
    new_phone = message.text
    db.edit_curator(data["curator_id"], None, new_phone)
    await bot.send_message(message.from_user.id, "Телефонный номер куратора успешно изменен")
    await state.finish()


@dp.callback_query_handler(lambda c: c.data and c.data.startswith("curator_"), state=DelCurator.init)
async def rm_curator(callback: types.CallbackQuery, state: FSMContext):
    curator_id = callback.data.split("curator_")[1]
    db.rm_curator_by_id(curator_id)

    await bot.send_message(callback.from_user.id, "Куратор успешно удален", reply_markup=kb.back_keyboard)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith("category_"), state=AddProduct.waiting_for_category)
async def process_new_product_category(callback: types.CallbackQuery, state: FSMContext):
    category_id = callback.data.split("category_")[1]
    await state.update_data(category=category_id)
    await bot.send_message(callback.from_user.id, "Введите название товара")
    await AddProduct.waiting_for_name.set()


@dp.message_handler(state=AddProduct.waiting_for_name, content_types=types.ContentType.TEXT)
async def process_new_product_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await bot.send_message(message.from_user.id, "Введите описание")
    await AddProduct.waiting_for_description.set()


@dp.message_handler(state=AddProduct.waiting_for_description, content_types=types.ContentType.TEXT)
async def process_new_product_description(message: types.Message, state: FSMContext):
    description = message.text
    await state.update_data(description=description)
    await bot.send_message(message.from_user.id, "Введите цену или отправьте команду /skip")
    await AddProduct.waiting_for_price.set()


@dp.message_handler(state=AddProduct.waiting_for_price, content_types=types.ContentType.TEXT)
async def process_new_product_price(message: types.Message, state: FSMContext):
    if "skip" not in message.text:
        price = float(message.text)
        await state.update_data(price=price)
    await bot.send_message(message.from_user.id, "Введите цену со скидкой или отправьте команду /skip")
    await AddProduct.waiting_for_discount_price.set()


@dp.message_handler(state=AddProduct.waiting_for_discount_price, content_types=types.ContentType.TEXT)
async def process_new_product_price(message: types.Message, state: FSMContext):
    if "skip" not in message.text:
        price_discount = float(message.text)
        await state.update_data(price_discount=price_discount)
    await bot.send_message(message.from_user.id, "Прикрепите изображение товара или отправьте команду /skip")
    await AddProduct.waiting_for_image.set()


@dp.message_handler(state=AddProduct.waiting_for_image, content_types=[types.ContentType.PHOTO, types.ContentType.TEXT])
async def process_new_product_image(message: types.Message, state: FSMContext):
    if message.content_type == types.ContentType.PHOTO:
        photo_id = message.photo[-1].file_id
        await state.update_data(image=photo_id)
        await bot.send_message(message.from_user.id, "Вставьте ссылку на товар или отправьте команду /skip")
        await AddProduct.waiting_for_link.set()
    elif "skip" in message.text:
        await bot.send_message(message.from_user.id, "Вставьте ссылку на товар или отправьте команду /skip")
        await AddProduct.waiting_for_link.set()
    else:
        await bot.send_message(message.from_user.id, "Прикрепите изображение товара или отправьте команду /skip")


@dp.message_handler(state=AddProduct.waiting_for_link, content_types=[types.ContentType.PHOTO, types.ContentType.TEXT])
async def process_new_product_link(message: types.Message, state: FSMContext):
    if "skip" not in message.text:
        link = message.text
        await state.update_data(link=link)
    await bot.send_message(message.from_user.id, "Вставьте содержание товара или отправьте команду /skip")
    await AddProduct.waiting_for_content.set()


@dp.message_handler(state=AddProduct.waiting_for_content, content_types=types.ContentType.TEXT)
async def process_new_product_content(message: types.Message, state: FSMContext):
    if "skip" not in message.text:
        content = message.text
        await state.update_data(content=content)

    data = await state.get_data()
    product = db.save_product(
        category=data["category"],
        name=data["name"],
        description=data["description"],
        price=data.get("price", None),
        price_discount=data.get("price_discount", None),
        image=data.get("image", None),
        link=data.get("link", None),
        content=data.get("content", None),
    )
    await state.finish()
    await AddLesson.init.set()
    await bot.send_message(
        message.from_user.id,
        "Товар успешно добавлен",
        reply_markup=kb.generate_product_add_lessons_keyboard(product.id),
    )


@dp.callback_query_handler(lambda c: c.data and c.data.startswith("lessons_add_for_product_"), state=AddLesson.init)
async def process_lesson(callback: types.CallbackQuery, state: FSMContext):
    product_id = callback.data.split("lessons_add_for_product_")[1]
    await state.update_data(product_id=product_id)
    await bot.send_message(callback.from_user.id, "Отправьте фото урока или команду /skip")
    await AddLesson.waiting_for_photo.set()


@dp.callback_query_handler(lambda c: c.data and c.data.startswith("lessons_skip_for_product_"), state=AddLesson.init)
async def process_lesson(callback: types.CallbackQuery, state: FSMContext):
    await bot.send_message(
        callback.from_user.id, "Пропускаем добавление уроков", reply_markup=new_product_and_admin_panel_kb
    )
    await state.finish()


@dp.message_handler(state=AddLesson.waiting_for_photo, content_types=[types.ContentType.PHOTO, types.ContentType.TEXT])
async def process_lesson(message: types.Message, state: FSMContext):
    if message.content_type == types.ContentType.PHOTO:
        photo = message.photo[-1].file_id
        await state.update_data(photo=photo)
        await bot.send_message(message.from_user.id, "Вставьте анимацию для урока или отправьте команду /skip")
        await AddLesson.waiting_for_gif.set()
    elif message.content_type == types.ContentType.TEXT and "skip" in message.text:
        await bot.send_message(message.from_user.id, "Вставьте анимацию для урока или отправьте команду /skip")
        await AddLesson.waiting_for_gif.set()
    elif message.content_type == types.ContentType.TEXT and "finish" in message.text:
        await bot.send_message(
            message.from_user.id, "Уроки успешно добавлены", reply_markup=new_product_and_admin_panel_kb
        )
        await state.finish()
    else:
        await bot.send_message(message.from_user.id, "Отправьте фото урока или команду /skip")


@dp.message_handler(
    state=AddLesson.waiting_for_gif, content_types=[types.ContentType.ANIMATION, types.ContentType.TEXT]
)
async def process_lesson(message: types.Message, state: FSMContext):
    if message.content_type == types.ContentType.ANIMATION:
        gif = message.animation.file_id
        await state.update_data(gif=gif)
        await bot.send_message(message.from_user.id, "Добавьте файл для урока или отправьте команду /skip")
        await AddLesson.waiting_for_document.set()
    elif message.content_type == types.ContentType.TEXT and "skip" in message.text:
        await bot.send_message(message.from_user.id, "Добавьте файл для урока или отправьте команду /skip")
        await AddLesson.waiting_for_document.set()


@dp.message_handler(
    state=AddLesson.waiting_for_document, content_types=[types.ContentType.DOCUMENT, types.ContentType.TEXT]
)
async def process_lesson(message: types.Message, state: FSMContext):
    if message.content_type == types.ContentType.DOCUMENT:
        document = message.document.file_id
        await state.update_data(document=document)
        await bot.send_message(message.from_user.id, "Добавьте контент урока или отправьте команду /skip")
        await AddLesson.waiting_for_content.set()
    elif message.content_type == types.ContentType.TEXT and "skip" in message.text:
        await bot.send_message(message.from_user.id, "Добавьте контент урока или отправьте команду /skip")
        await AddLesson.waiting_for_content.set()


@dp.message_handler(state=AddLesson.waiting_for_content, content_types=types.ContentType.TEXT)
async def process_lesson(message: types.Message, state: FSMContext):
    # process content
    if "skip" not in message.text:
        await state.update_data(content=message.text)

    # when we filled in the lesson's photo, gif, link, content we save the lesson here as a final step
    data = await state.get_data()
    if "order" in data:
        await state.update_data(order=data["order"] + 1)
    else:
        await state.update_data(order=1)
    data = await state.get_data()

    lesson = db.save_lesson(
        content=data.get("content", None),
        photo=data.get("photo", None),
        gif=data.get("gif", None),
        document=data.get("document", None),
    )

    db.save_product_lesson(product_id=data["product_id"], lesson_id=lesson.id, order=data["order"])

    await bot.send_message(
        message.from_user.id,
        "Отправьте фото следующего урока или отправьте команду /skip.\n"
        "Закончить добавление уроков можно командой /finish",
    )
    await AddLesson.waiting_for_photo.set()


@dp.callback_query_handler(lambda c: c.data and c.data.startswith("category_"), state=EditProduct.waiting_for_category)
async def process_edit_product_category(callback: types.CallbackQuery, state: FSMContext):
    category_id = callback.data.split("category_")[1]
    await bot.send_message(
        callback.from_user.id,
        "Выберите продукт для изменения",
        reply_markup=kb.generate_product_keyboard(category_id, False),
    )
    await EditProduct.waiting_for_product.set()


@dp.callback_query_handler(lambda c: c.data and c.data.startswith("product_"), state=EditProduct.waiting_for_product)
async def process_edit_product_product(callback: types.CallbackQuery, state: FSMContext):
    product_id = callback.data.split("product_")[1]
    await state.update_data(product_id=product_id)
    await bot.send_message(callback.from_user.id, "Что вы хотите изменить?", reply_markup=kb.generate_edit_product())
    await EditProduct.waiting_for_column.set()


@dp.callback_query_handler(lambda c: c.data, state=EditProduct.waiting_for_column)
async def process_edit_product_column(callback: types.CallbackQuery, state: FSMContext):
    column_name = callback.data
    if column_name == "lessons":
        data = await state.get_data()
        await bot.send_message(
            callback.from_user.id,
            "Выберите, какой урок хотите изменить",
            reply_markup=kb.generate_product_lessons(data["product_id"]),
        )
        await state.finish()
        await EditLesson.waiting_for_lesson.set()
    else:
        await state.update_data(column_name=column_name)
        await bot.send_message(callback.from_user.id, "Введите новое значение")
        await EditProduct.waiting_for_new_value.set()


@dp.message_handler(
    state=EditProduct.waiting_for_new_value, content_types=[types.ContentType.PHOTO, types.ContentType.TEXT]
)
async def process_edit_product_new_value(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if message.content_type == types.ContentType.PHOTO:
        new_value = message.photo[-1].file_id
    else:
        new_value = message.text
    db.edit_product(data["product_id"], data["column_name"], new_value)
    await bot.send_message(message.from_user.id, "Изменение сохранено")
    await state.finish()


@dp.callback_query_handler(lambda c: c.data, state=EditLesson.waiting_for_lesson)
async def process_edit_lesson(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(lesson_id=callback.data)
    await bot.send_message(
        callback.from_user.id, "Какое поле вы хотите изменить?", reply_markup=kb.generate_edit_lessons()
    )
    await EditLesson.waiting_for_column.set()


@dp.callback_query_handler(lambda c: c.data, state=EditLesson.waiting_for_column)
async def process_edit_lesson_column(callback: types.CallbackQuery, state: FSMContext):
    column_name = callback.data
    await state.update_data(column_name=column_name)
    await bot.send_message(callback.from_user.id, "Введите новое значение")
    await EditLesson.waiting_for_new_value.set()


@dp.message_handler(
    state=EditLesson.waiting_for_new_value,
    content_types=[
        types.ContentType.PHOTO,
        types.ContentType.TEXT,
        types.ContentType.ANIMATION,
        types.ContentType.DOCUMENT,
    ],
)
async def process_edit_lesson_value(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if message.content_type == types.ContentType.PHOTO:
        new_value = message.photo[-1].file_id
    elif message.content_type == types.ContentType.TEXT:
        new_value = message.text
    elif message.content_type == types.ContentType.ANIMATION:
        new_value = message.animation.file_id
    elif message.content_type == types.ContentType.DOCUMENT:
        new_value = message.document.file_id
    else:
        return
    db.edit_lesson(data["lesson_id"], data["column_name"], new_value)
    await bot.send_message(message.from_user.id, "Урок изменен")
    await state.finish()


@dp.callback_query_handler(
    lambda c: c.data and c.data.startswith("category_"), state=RemoveProduct.waiting_for_category
)
async def process_new_product_category(callback: types.CallbackQuery, state: FSMContext):
    category_id = callback.data.split("category_")[1]
    await bot.send_message(
        callback.from_user.id, "Выберите продукт для удаления", reply_markup=kb.generate_product_keyboard(category_id)
    )
    await RemoveProduct.waiting_for_product.set()


@dp.callback_query_handler(lambda c: c.data and c.data.startswith("product_"), state=RemoveProduct.waiting_for_product)
async def process_new_product_category(callback: types.CallbackQuery, state: FSMContext):
    product_id = callback.data.split("product_")[1]
    db.rm_product(product_id)
    await bot.send_message(callback.from_user.id, "Продукт успешно удален")
    await state.finish()


@dp.message_handler(state=AddVideo.waiting_for_name, content_types=types.ContentType.TEXT)
async def add_video(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await bot.send_message(message.from_user.id, f"Отправьте видео")
    await AddVideo.waiting_for_video.set()


@dp.message_handler(state=AddGif.waiting_for_name, content_types=types.ContentType.TEXT)
async def add_gif(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await bot.send_message(message.from_user.id, f"Отправьте анимацию")
    await AddGif.waiting_for_animation.set()


@dp.message_handler(state=AddGif.waiting_for_animation, content_types=types.ContentType.ANIMATION)
async def add_gif(message: types.Message, state: FSMContext):
    data = await state.get_data()
    name = data["name"]
    tg_id = message.animation.file_id
    db.create_gif(name, tg_id)
    await bot.send_message(message.from_user.id, f"Gif {name} [{tg_id}] успешно создана")
    await state.finish()


@dp.message_handler(state=AddVideo.waiting_for_video, content_types=types.ContentType.VIDEO)
async def add_video(message: types.Message, state: FSMContext):
    data = await state.get_data()
    name = data["name"]
    tg_id = message.video.file_id
    db.create_video(name, tg_id)
    await bot.send_message(message.from_user.id, f"Видео {name} [{tg_id}] успешно создано")
    await state.finish()


@dp.message_handler(state=AddPhoto.waiting_for_name, content_types=types.ContentType.TEXT)
async def add_photo_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await bot.send_message(message.from_user.id, f"Отправьте изображение")
    await AddPhoto.waiting_for_photo.set()


@dp.message_handler(state=AddPhoto.waiting_for_photo, content_types=types.ContentType.PHOTO)
async def add_photo(message: types.Message, state: FSMContext):
    data = await state.get_data()
    name = data["name"]
    tg_id = message.photo[-1].file_id
    db.create_photo(name, tg_id)
    await bot.send_message(message.from_user.id, f"Фото {name} [{tg_id}] успешно добавлено")
    await state.finish()


# диалоги для добавления учителя
@dp.message_handler(state=RegisterTeacher.waiting_for_name, content_types=types.ContentType.TEXT)
async def get_teacher_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await bot.send_message(message.from_user.id, "Введите телефон учителя")
    await RegisterTeacher.waiting_for_phone.set()


@dp.message_handler(state=RegisterTeacher.waiting_for_phone, content_types=types.ContentType.TEXT)
async def get_teacher_phone(message: types.Message, state: FSMContext):
    phone = Methods.validate_phone_number(message.text)
    if not phone:
        await bot.send_message(message.from_user.id, "Неверный формат номера")
        await RegisterTeacher.waiting_for_phone.set()
        return
    name = await state.get_data()
    name = name["name"]
    key = Methods.generate_secret_key()
    db.register_teacher(
        name, phone, key,
    )
    await bot.send_message(
        message.from_user.id, "Учитель создан, секретный ключ:\n" + key, reply_markup=kb.admin_main,
    )
    await state.finish()


# диалоги добавления админа
@dp.message_handler(state=Num.waiting_for_number, content_types=types.ContentType.TEXT)
async def register_admin(message: types.Message, state: FSMContext):
    num = Methods.validate_phone_number(message.text)
    if not num:
        await bot.send_message(message.from_user.id, "Неверно введен номер!")
        await Num.waiting_for_number.set()
        return
    if db.get_user_by_phone(num):
        db.get_user_by_phone(num).get().delete_instance()
    key = Methods.generate_secret_key()
    db.register_admin(num, key)
    await bot.send_message(message.from_user.id, Cfg.ADDED_ADMIN + key, reply_markup=kb.admin_main)
    await state.finish()
