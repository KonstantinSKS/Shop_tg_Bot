from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message

from tg_bot.db.db_commands import get_tg_user


class UserMiddleware(BaseMiddleware):
    """Middleware для проверки заблокированных пользователей."""

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        if event.from_user.is_bot is False:
            user = await get_tg_user(event.from_user.id)
            if user and user.is_unblocked is False:
                await event.answer(text='Вы заблокированы.', show_alert=True)
                return
            data['tg_user'] = user
        return await handler(event, data)
