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


@shoping_router.callback_query(  # StateUser.statistics,
                               F.data == "back_step")
@shoping_router.callback_query(F.data.startswith("categories_page_"))
@shoping_router.callback_query(F.data == "catalog")
async def get_categories(call: types.CallbackQuery):
    """Получение всех категорий товаров с пагинацией."""

    categories = await db.get_all_categories()
    if not categories:
        await call.message.answer("Категории пока отсутствуют.")
        return

    page = int(call.data.split("_")[-1]) if "categories_page_" in call.data else 1
    print("page:", page)
    print("call:", call)

    await call.message.edit_text(
        "Выберите категорию:",
        reply_markup=inline_kb.categories_kb(categories, page)
    )


@shoping_router.callback_query(F.data.startswith("category_"))
async def show_category(call: types.CallbackQuery):
    """Отображает категорию и список её подкатегорий с пагинацией."""

    data_parts = call.data.split("_")
    print("call:", call)
    print("data_parts:", data_parts)
    category_id = int(data_parts[1])
    print("category_id:", category_id)
    page = int(data_parts[3]) if len(data_parts) > 3 else 1
    print("page:", page)

    category = await db.get_category(category_id)
    subcategories = await db.get_all_subcategories(category_id)

    if not category:
        await call.answer("Категория не найдена!", show_alert=True)
        return

    text = f"*{category.title}*\n\nВыберите подкатегорию:"
    keyboard = inline_kb.subcategories_kb(subcategories, category_id, page)

    await call.message.edit_text(
        text=text,
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
