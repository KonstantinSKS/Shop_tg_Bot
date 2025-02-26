import asyncio
from aiogram.types import BotCommand

from tg_bot.loader import dp, bot
from tg_bot.config import super_user_name, super_user_pass
from tg_bot.middlewares.blocking import UserMiddleware
from tg_bot.settings_logger import logger
from tg_bot.db.db_commands import create_super_user


async def set_commands():
    """Функция для формирования списка команд для кнопки Menu."""

    commands = [BotCommand(command="/start", description="Запустить бота"),
                BotCommand(command="/help", description="Помощь"),]
    await bot.set_my_commands(commands=commands)


async def main():
    """Функция запуска бота."""

    logger.info('Запуск бота')

    await create_super_user(super_user_name, super_user_pass)

    await set_commands()

    dp.message.outer_middleware(UserMiddleware())
    dp.callback_query.outer_middleware(UserMiddleware())

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
