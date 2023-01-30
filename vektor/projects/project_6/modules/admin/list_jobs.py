from aiogram import types
from apscheduler.job import Job
from apscheduler.triggers.date import DateTrigger

from loader import dp, scheduler
from modules.BotKeyboards import admin_dt, generate_jobs_kb, jobs_kb_data, manage_job_data, \
    generate_manage_job_keyboard, generate_accept_delete, accept_delete_job_data, mailing_keyboard
from modules.DataBase import get_name_product
from modules.calendar_kb import generate_calendar_jobs_kb, calendar_info_data_jobs, control_months_data_jobs


@dp.callback_query_handler(text='mailing_schedule_back')
async def process_mailing_schedule_back(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text('Выберете метод рассылки', reply_markup=mailing_keyboard)



@dp.callback_query_handler(calendar_info_data_jobs.filter(prefix="day", day="null"))
async def process_null_day(call: types.CallbackQuery, callback_data: dict):
    await call.answer(cache_time=1, text=f"Такого дня нет")


@dp.callback_query_handler(admin_dt.filter(prefix='list_jobs'))
async def process_get_all_jobs(call: types.CallbackQuery):
    await call.answer()
    accept_jobs = []
    all_jobs = scheduler.get_jobs()
    for job in all_jobs:
        if job.name == 'scheduler-jobs':
            accept_jobs.append(job)
    await call.message.edit_text('Выберете дату', reply_markup=generate_calendar_jobs_kb(accept_jobs))


@dp.callback_query_handler(calendar_info_data_jobs.filter(have_jobs='yes'))
async def process_getting_jobs_on_date(call: types.CallbackQuery, callback_data: dict):
    month = int(callback_data.get("month"))
    year = int(callback_data.get("year"))
    day = int(callback_data.get("day"))
    all_jobs = scheduler.get_jobs()
    jobs_on_date = []
    for job in all_jobs:
        job_date = job.next_run_time
        if job_date.year == year and job_date.month == month and job_date.day == day and job.name == 'scheduler-jobs':
            jobs_on_date.append(job.id)
    await call.message.edit_text('Выберете рассылку:', reply_markup=generate_jobs_kb(jobs_on_date))
    await call.answer(cache_time=1)


@dp.callback_query_handler(calendar_info_data_jobs.filter())
async def process_not_letter(call: types.CallbackQuery):
    await call.answer(cache_time=1, text=f"На этот день нет рассылки")


@dp.callback_query_handler(jobs_kb_data.filter(job_id='back'))
async def back_job(call: types.CallbackQuery):
    await call.answer()
    accept_jobs = []
    all_jobs = scheduler.get_jobs()
    for job in all_jobs:
        if job.name == 'scheduler-jobs':
            accept_jobs.append(job)
    await call.message.edit_text('Выберете дату', reply_markup=generate_calendar_jobs_kb(accept_jobs))


@dp.callback_query_handler(jobs_kb_data.filter())
async def get_job(call: types.CallbackQuery, callback_data: dict):
    job_id = callback_data.get('job_id')
    job = scheduler.get_job(job_id)
    await call.message.delete()
    await get_job_info(job, call.message)
    await call.answer()


@dp.callback_query_handler(manage_job_data.filter(prefix='back'))
async def back_to_change_time(call: types.CallbackQuery, callback_data: dict):
    job = scheduler.get_job(callback_data.get('job_id'))
    await call.message.delete()
    month = job.next_run_time.month
    year = job.next_run_time.year
    day = job.next_run_time.day
    all_jobs = scheduler.get_jobs()
    jobs_on_date = []
    for job in all_jobs:
        job_date = job.next_run_time
        if job_date.year == year and job_date.month == month and job_date.day == day:
            jobs_on_date.append(job.id)
    await call.message.answer('Выберете рассылку:', reply_markup=generate_jobs_kb(jobs_on_date))
    await call.answer(cache_time=1)


@dp.callback_query_handler(manage_job_data.filter(prefix='delete'))
async def accept_delete_job(call: types.CallbackQuery, callback_data: dict):
    text = 'Вы точно хотите удалить эту рассылку'
    job_id = callback_data.get('job_id')
    await call.message.delete()
    await call.message.answer(text, reply_markup=generate_accept_delete(job_id))
    await call.answer(cache_time=1)


@dp.callback_query_handler(accept_delete_job_data.filter(prefix='yes'))
async def delete_job(call: types.CallbackQuery, callback_data: dict):
    text = 'Рассылка успешно удалена'
    job_id = callback_data.get('job_id')
    job = scheduler.get_job(job_id=job_id)
    job.remove()
    await call.message.delete()
    accept_jobs = []
    all_jobs = scheduler.get_jobs()
    for job in all_jobs:
        if job.name == 'scheduler-jobs':
            accept_jobs.append(job)
    await call.answer()
    await call.message.answer(f'{text}\nВыберете дату', reply_markup=generate_calendar_jobs_kb(accept_jobs))


@dp.callback_query_handler(accept_delete_job_data.filter(prefix='no'))
async def delete_job(call: types.CallbackQuery, callback_data: dict):
    job_id = callback_data.get('job_id')
    job = scheduler.get_job(job_id=job_id)
    await call.answer()
    await call.message.delete()
    await get_job_info(job, call.message)


@dp.callback_query_handler(control_months_data_jobs.filter(prefix="next"))
async def process_get_next_month(call: types.CallbackQuery, callback_data: dict):
    month = int(callback_data.get("month")) + 1
    year = int(callback_data.get("year"))
    if month > 12:
        month = 1
        year += 1
    accept_jobs = []
    all_jobs = scheduler.get_jobs()
    for job in all_jobs:
        if job.name == 'scheduler-jobs':
            accept_jobs.append(job)

    calendar = generate_calendar_jobs_kb(accept_jobs, year, month)
    await call.message.edit_reply_markup(reply_markup=calendar)


@dp.callback_query_handler(control_months_data_jobs.filter(prefix="prev"))
async def process_get_next_month(call: types.CallbackQuery, callback_data: dict):
    await call.answer(cache_time=0)
    month = int(callback_data.get("month")) - 1
    year = int(callback_data.get("year"))
    if month < 1:
        month = 12
        year -= 1
    accept_jobs = []
    all_jobs = scheduler.get_jobs()
    for job in all_jobs:
        if job.name == 'scheduler-jobs':
            accept_jobs.append(job)

    calendar = generate_calendar_jobs_kb(accept_jobs, year, month)
    await call.message.edit_reply_markup(reply_markup=calendar)


async def get_job_info(job: Job, message: types.Message):
    args = job.args
    keyborad = generate_manage_job_keyboard(job.id)

    message_text = args[0]
    data = args[1]
    image = args[2]
    document = args[3]
    animation = args[4]
    link = args[5]
    text_link = args[6]
    if type(job.trigger) == DateTrigger:
        text = f'Тип: по дате\n'
    else:
        text = 'Тип: повторяющаяся\n'
    who = await get_type_data(data)
    text += f'Кому: {who}\n\n'
    if link:
        text += f'Ссылка: {link}\n'
        if text_link:
            text += f'Текст ссылки: "{text_link}"\n\n'
        else:
            text += f'Текст ссылки: "Ссылка"\n\n'
    text += f'Текст сообщения:\n{message_text}'
    if document:
        await message.answer_document(document=document, caption=text, reply_markup=keyborad)
        return
    if animation:
        await message.answer_animation(animation=animation, caption=text, reply_markup=keyborad)
        return
    if image:
        await message.answer_photo(photo=image, caption=text, reply_markup=keyborad)
        return
    await message.answer(text, reply_markup=keyborad)


async def get_type_data(data):
    if data == "all":
        return 'всем'
    elif data == "entrance_test":
        return 'прошедшим входное тестирование'
    elif data == "not_moms":
        return 'Не мамам'
    elif data == "pregnant":
        return 'Беременным'
    elif data == "moms":
        return 'Мамам'
    elif data == "first_stage":
        return 'На 1 стадии'
    elif data == "second_stage":
        return 'На 2 стадии'
    elif data == "third_stage":
        return 'На 3 стадии'
    elif data.startswith("bought_product_"):
        product_id = int(data.split("bought_product_")[1])
        product_name = get_name_product(product_id)
        return f'купившим {product_name}'
    elif data.startswith("not_bought_product_"):
        product_id = int(data.split("not_bought_product_")[1])
        product_name = get_name_product(product_id)
        return f'Не купившим {product_name}'

    return 'всем'
