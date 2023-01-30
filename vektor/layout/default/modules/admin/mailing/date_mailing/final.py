from loader import bot
from modules.BotKeyboards import date_mailing_keyboard


async def final_message(data, chat):
    year = int(data['year'])
    month = int(data['month'])
    day = int(data['day'])
    hour = int(data['hour'])
    minute = int(data['minute'])
    message_text = data['message_text']
    photo = data['photo']
    document = data['document']
    animation = data['animation']
    link = data['link']
    text_link = data['text_link']
    text = f'Время отправки {day}-{month}-{year} {hour}:{minute}\n\n' \
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
