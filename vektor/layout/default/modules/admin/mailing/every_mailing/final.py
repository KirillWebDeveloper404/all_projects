from loader import bot
from modules.BotKeyboards import date_mailing_keyboard


async def final_message(data, chat):
    every_day = data['every_day']
    every_day_of_week = data['every_day_of_week']
    every_month = data['every_month']
    day_of_month = data['day_of_month']
    day_of_week = data['day_of_week']
    hour = int(data['hour'])
    minute = int(data['minute'])
    message_text = data['message_text']
    photo = data['photo']
    document = data['document']
    animation = data['animation']
    link = data['link']
    text_link = data['text_link']
    text = ''
    if every_day:
        text += 'Метод: каждый день\n'
    if every_month:
        text += f'Метод: каждый месяц {day_of_month} числа\n'
    if every_day_of_week:
        text_day_of_week = await get_text_day_of_week(day_of_week)
        text += f'Метод: каждую неделю в {text_day_of_week}\n'

    text += f'Время отправки: {hour}:{minute}\n\n' \
            f'Сообщение:\n' \
            f'{message_text}'
    if link:
        text += f'\n\n Ссылка: {link}\n'
        if text_link:
            text += f'Текст ссылки {text_link}'
        else:
            text += f'Текст ссылки "Ссылка"'

    if photo:
        await bot.send_photo(chat_id=chat, caption=text, photo=photo, reply_markup=date_mailing_keyboard)
    elif document:
        await bot.send_document(chat_id=chat, document=document, caption=text, reply_markup=date_mailing_keyboard)
    elif animation:
        await bot.send_animation(chat_id=chat, animation=animation, caption=text, reply_markup=date_mailing_keyboard)
    else:
        await bot.send_message(chat_id=chat, text=text, reply_markup=date_mailing_keyboard)


async def get_text_day_of_week(day):
    week = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресеье']
    return week[day]
