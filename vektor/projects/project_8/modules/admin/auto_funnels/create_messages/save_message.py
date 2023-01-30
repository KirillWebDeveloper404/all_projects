from loader import scheduler
from modules.DataBase import create_msg_af
from utils.functions.send_message_funnel import send_message_funnel


async def save_message(data):
    photo = data['photo']
    gif = data['gif']
    video = data['video']
    video_note = data['video_note']
    audio = data['audio']
    voice = data['voice']
    document = data['document']
    type_message = data['type']
    day = data['day']
    hour = data['hour']
    minute = data['minute']
    msg_text = data['text']
    interval_msg = data['interval_msg']
    delete_hour = data['delete_hour']
    delete_minute = data['delete_minute']
    delete_day = data['delete_day']
    delete_second = data['delete_second']
    link = data['link']
    funnel_id = data['funnel_id']
    interval_second = data['interval_second']
    interval_day = data['interval_day']
    interval_hour = data['interval_hour']
    interval_minute = data['interval_minute']
    text_link = data['text_link']
    test = data['test']

    is_first = False
    if type_message == 'first':
        is_first = True
        type_message = 'content'
    if type_message == 'system':
        day = day * -1
    msg = create_msg_af(funnel_id=funnel_id,
                        type_message=type_message,
                        message_text=msg_text,
                        photo=photo,
                        gif=gif,
                        video=video,
                        voice=voice,
                        video_note=video_note,
                        document=document,
                        audio=audio,
                        day=day,
                        hour=hour,
                        minute=minute,
                        interval_msg_id=interval_msg,
                        interval_hour=interval_hour,
                        interval_minute=interval_minute,
                        interval_day=interval_day,
                        interval_second=interval_second,
                        delete_hour=delete_hour,
                        delete_day=delete_day,
                        delete_second=delete_second,
                        delete_minute=delete_minute,
                        link=link,
                        text_link=text_link,
                        is_first=is_first,
                        test=test
                        )
    if not interval_msg and not is_first:
        scheduler.add_job(send_message_funnel, 'cron', hour=hour, minute=minute, args=(msg.id,),
                          name=f'message_af_{msg.id}')
    return funnel_id
