import datetime

import peewee
import pytz

from data.config import DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME, TIME_ZONE

db_handler = peewee.SqliteDatabase('bot.db')


class BaseModel(peewee.Model):
    id = peewee.PrimaryKeyField()

    # базовая модель без времени, от нее наследованы все остальные модели
    class Meta:
        database = db_handler


class BaseTSModel(BaseModel):
    tz = pytz.timezone(TIME_ZONE)
    ts = peewee.DateTimeField(default=datetime.datetime.now(tz))


