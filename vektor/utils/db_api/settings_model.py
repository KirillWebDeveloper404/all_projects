from peewee import TextField

from utils.db_api.base import BaseModel


class Settings(BaseModel):
    site = TextField(null=True)
    channel = TextField(null=True)
    helper = TextField(null=True)
    chat = TextField(null=True)

    class Meta:
        table_name = 'settings'


async def create_default():
    try:
        setings = Settings()
        setings.save()
    except Exception:
        pass


async def get_settings():
    return Settings.select().where(Settings.id == 1).get()


async def change_settings(site=None, channel=None, helper=None, chat=None):
    setting = Settings.select().where(Settings.id == 1).get()
    if site:
        setting.site = site
    if channel:
        setting.channel = channel
    if helper:
        setting.helper = helper
    if chat:
        setting.chat = chat
    setting.save()
    return setting
