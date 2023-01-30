import pytz
from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

ADMINS = env.list("ADMINS")
BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
DB_PASS = env.str("DB_PASS")  # Забираем значение типа str
DB_USER = env.str("DB_USER")  # Забираем значение типа str
DB_PORT = env.str("DB_PORT")  # Забираем значение типа str
DB = env.str("DB")  # Забираем значение типа str
DB_HOST = env.str("DB_HOST")  # Забираем значение типа str
TIME_ZONE = env.str("TIME_ZONE")
UTC_TIME_ZONE = pytz.timezone(env.str("UTC_TIME_ZONE"))


