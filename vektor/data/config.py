from environs import Env
from pathlib import Path
# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
PAYMENTS_PROVIDER_TOKEN = env.str("PAY_TOKEN")
DB_PASS='Vecto023'
DB_USER='vector'
DB_PORT=5432
DB_HOST='127.0.0.1'
DB_NAME='vector '
PAY_TOKEN='390540012:LIVE:17553'
ADMINS=1691052907
TIME_ZONE="Europe/Moscow"
CHAT_ID=1691052907
