import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, Redis
from aiogram.client.default import DefaultBotProperties
import django

from tg_bot.config import BOT_TOKEN, redis_host, redis_port
from tg_bot.settings_logger import logger


def setup_django():
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "admin_panel.django_settings.settings"
    )
    os.environ.update({"DJANGO_ALLOW_ASYNC_UNSAFE": "true"})
    django.setup()


def include_all_routers():
    from tg_bot.handlers import all_handlers
    for handler in all_handlers:
        dp.include_router(handler)


logger.info("Logger initialized")
setup_django()

bot = Bot(
    BOT_TOKEN,
    default=DefaultBotProperties(
        parse_mode="HTML")
    )

if redis_host and redis_port:
    storage = RedisStorage(Redis(host=redis_host, port=redis_port))
else:
    storage = MemoryStorage()

dp = Dispatcher(storage=storage)
include_all_routers()
