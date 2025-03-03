
from aiogram.types import FSInputFile
# from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hbold, hitalic
# from aiogram.types import InlineKeyboardMarkup
from aiogram import types, Router, F
# from aiogram.filters import Command
# from aiogram.exceptions import TelegramBadRequest

from tg_bot.db import db_commands as db
# from tg_bot.loader import bot
# from tg_bot.settings_logger import logger
# from tg_bot.states.all_states import StateUser
from tg_bot.keyboards import inline as inline_kb
from tg_bot.keyboards.callback_data import (
    CategoriesCallback, ProductItemCallback, SubcategoryCallback, ProductCallback)
# from tg_bot.misc.utils import check_sub_channel
# from tg_bot.misc import constants as const


shoping_router = Router()


@shoping_router.callback_query(CategoriesCallback.filter())
async def get_categories(call: types.CallbackQuery, callback_data: CategoriesCallback):
    """Получение всех категорий товаров с пагинацией."""

    categories = await db.get_all_categories()
    if not categories:
        await call.message.answer("Категории пока отсутствуют.") # cache_time=3
        return

    text = "Выберите категорию:"
    keyboard = inline_kb.categories_kb(categories, callback_data.page)
    await call.message.edit_text(
        text,
        reply_markup=keyboard
    )


@shoping_router.callback_query(SubcategoryCallback.filter())
async def show_category(call: types.CallbackQuery, callback_data: SubcategoryCallback):
    """Отображает категорию и список её подкатегорий с пагинацией."""

    category = await db.get_category(callback_data.category_id)
    subcategories = await db.get_all_subcategories(callback_data.category_id)
    if not subcategories:
        await call.message.answer("Подкатегории пока отсутствуют.") #cache_time=3
        return

    text = f"*{category.title}*\n\nВыберите подкатегорию:"
    keyboard = inline_kb.subcategories_kb(
        subcategories, callback_data.category_id, callback_data.page
    )

    if call.message.photo:
        await call.message.delete()
        await call.message.answer(
            text=text,
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
    else:
        await call.message.edit_text(
            text=text,
            reply_markup=keyboard,
            parse_mode="Markdown"
        )


@shoping_router.callback_query(ProductItemCallback.filter())
async def show_product(call: types.CallbackQuery, callback_data: ProductItemCallback):
    """Обрабатывает нажатие на кнопку подкатегории и выводит товары."""

    products = await db.get_all_products(callback_data.subcategory_id)
    if not products:
        await call.message.answer("❌ В этой категории пока нет товаров.")
        return

    products = list(products)
    total_products = len(products)
    product_index = callback_data.product_index
    product = products[product_index - 1]

    text = f"{hbold(product.title)}\n{hitalic(product.description)}\n💰 Цена: {product.price} р."
    keyboard = inline_kb.product_item_kb(
        subcategory_id=callback_data.subcategory_id,
        product_index=product_index,
        total_products=total_products,
        category_id=product.subcategory.category.id
    )

    if product.image:
        photo = FSInputFile(product.image.path)
        await call.message.edit_media(
                media=types.InputMediaPhoto(media=photo, caption=text),
                reply_markup=keyboard
            )
    else:
        await call.message.answer(
                text=text,
                reply_markup=keyboard
            )
