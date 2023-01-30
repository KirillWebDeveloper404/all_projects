import datetime
import random
import re
import string

from loader import bot


def generate_secret_key():
    """
    генерирует секретный ключ для верификации
    """
    return "".join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(32))


def validate_phone_number(number_in_string):
    """
    проверяет, что телефон (num) имеет верный формат, убирает первую цифру и возвращает
    отредактированный номер или номер без изменений, когда номер не РФ
    """
    number_in_string = number_in_string.strip()
    if "+7" == number_in_string[:2] and number_in_string[1:].isdigit():
        return number_in_string[2:]
    elif "8" == number_in_string[0] or "7" == number_in_string[0]:
        return number_in_string[1:]
    else:
        return number_in_string


def validate_date_or_none(date_string):
    """
    валидитрует дату и возвращает объект datetime.date или None если формат неверный
    """
    if (
        re.match(r"\d{4}.\d{1,2}.\d{1,2}", date_string)
        and 0 <= int(date_string.split(".")[0]) <= 9999
        and 0 <= int(date_string.split(".")[1]) <= 12
        and 0 <= int(date_string.split(".")[2]) <= 31
    ):
        return datetime.date(
            int(date_string.split(".")[0]), int(date_string.split(".")[1]), int(date_string.split(".")[2]),
        )
    return None


def questions_to_db(question, correct_answer, another_answer, another_answer2, another_answer3):
    """
    создает и возвращает словарик с тестом для видеокурса для бд
    """
    s = str(len(question))
    s += question
    s += str(len(correct_answer))
    s += correct_answer
    s += str(len(another_answer))
    s += another_answer
    s += str(len(another_answer2))
    s += another_answer2
    s += str(len(another_answer3))
    s += another_answer3
    return s


def gen_promo(tchr_name=None):
    """
    создает промокод с именем учителя в коцне, или без имени - для любого учителя
    """
    promo_code = "".join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))
    if tchr_name:
        promo_code = f"{promo_code}{tchr_name}"
    return promo_code


def add_month(date):
    """
    добавляет к дате один месяц
    """
    if date.month + 1 <= 12:
        return datetime.date(date.year, date.month + 1, date.day)
    else:
        return datetime.date(date.year + 1, 1, date.day)


def add_two_times(time1, time2):
    """
    складывает два времени
    """
    # dummy: year, month, day, seconds; real: hours, minutes
    t = datetime.datetime(1000, 1, 1, time1.hour, time1.minute, 0)
    # add 0 days and so many seconds
    t += datetime.timedelta(0, time2.hour * 3600 + time2.minute * 60)
    return t.time()


def validate_time_or_none(time_string):
    """
    валидирует время и возвращает объект time
    """
    if (
        re.match(r"\d{1,2}:\d{1,2}", time_string)
        and 0 <= int(time_string.split(":")[0]) <= 23
        and 0 <= int(time_string.split(":")[1]) <= 59
    ):
        return datetime.time(int(time_string.split(":")[0]), int(time_string.split(":")[1]),)
    return None


def is_url_valid(url):
    url_regex = re.compile(
        r"^(?:http|ftp)s?://"  # http:// or https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain
        r"localhost|"  # localhost
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # or ip
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )
    return re.match(url_regex, url) is not None


