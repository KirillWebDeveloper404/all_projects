from modules.DataBase import get_answers_question


async def get_main_msg_question(question_id) -> str:
    answers = get_answers_question(question_id)

    text = ''
    if answers:
        question_text = answers[0].question.text
        text += f'Вопрос: {question_text}\nОтветы\n\n'
        for i in range(len(answers)):
            text += f'Ответ {i + 1}: {answers[i].text}\n'
    return text
