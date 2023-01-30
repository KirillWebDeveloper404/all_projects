from modules.DataBase import add_result_test


async def save_result(data):
    answer_id = data['answer_id']
    result_text = data['result_text']
    photo = data['photo']
    gif = data['gif']
    video = data['video']
    audio = data['audio']
    voice = data['voice']
    video_note = data['video_note']
    test = data['test']
    document = data['document']
    link = data['link']
    text_link = data['text_link']
    if result_text or photo or gif or video or audio or voice or video_note or test or document:
        add_result_test(answer_id, result_text, photo, gif, video, voice, video_note, document, audio, link, text_link,
                        test)
