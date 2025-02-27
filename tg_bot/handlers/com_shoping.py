from aiogram.fsm.context import FSMContext
from aiogram import types, Router, F
from aiogram.filters import Command

from tg_bot.db import db_commands as db
from tg_bot.loader import bot
from tg_bot.settings_logger import logger
# from tg_bot.states.all_states import StateUser
from tg_bot.keyboards import inline as inline_kb
from tg_bot.misc.utils import check_sub_channel
from tg_bot.misc import constants as const


shoping_router = Router()


@shoping_router.callback_query(F.data == "catalog")
async def get_categories(call: types.CallbackQuery):
    """Получение всех категорий товаров."""

    # await call.message.delete()
    categories = await db.get_all_categories()

    if not categories:
        await call.message.answer("Категории пока отсутствуют.")
        return

    # keyboard = inline_kb.builder_back_step_and_main_menu()
    await call.message.edit_text(
        "Выберите категорию:",
        reply_markup=inline_kb.create_categories_kb(categories)
    )
