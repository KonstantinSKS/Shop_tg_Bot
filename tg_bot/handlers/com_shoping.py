import os

# from admin_panel.django_settings.settings import MEDIA_ROOT
from admin_panel.django_settings import settings

from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hbold, hitalic
from aiogram.types import InlineKeyboardMarkup
from aiogram import types, Router, F
from aiogram.filters import Command

from tg_bot.db import db_commands as db
from tg_bot.loader import bot
from tg_bot.settings_logger import logger
# from tg_bot.states.all_states import StateUser
from tg_bot.keyboards import inline as inline_kb
from tg_bot.misc.utils import check_sub_channel
from tg_bot.misc import constants as const
from tg_bot.keyboards.pagination import paginate_products


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

    await call.message.edit_text(
        "Выберите категорию:",
        reply_markup=inline_kb.categories_kb(categories, page)
    )


@shoping_router.callback_query(F.data.startswith("category_"))
async def show_category(call: types.CallbackQuery):
    """Отображает категорию и список её подкатегорий с пагинацией."""

    data_parts = call.data.split("_")
    category_id = int(data_parts[1])
    page = int(data_parts[3]) if len(data_parts) > 3 else 1

    category = await db.get_category(category_id)
    subcategories = await db.get_all_subcategories(category_id)
    if not subcategories:
        await call.message.answer("Подкатегории пока отсутствуют.")
        return

    text = f"*{category.title}*\n\nВыберите подкатегорию:"
    keyboard = inline_kb.subcategories_kb(subcategories, category_id, page)

    await call.message.edit_text(
        text=text,
        reply_markup=keyboard,
        parse_mode="Markdown"
    )


# @shoping_router.callback_query(F.data.startswith("subcategory_"))
# async def show_subcategory(call: types.CallbackQuery):
#     """Отображает подкатегорию и список её товаров с пагинацией."""

#     print("call:", call)
#     data_parts = call.data.split("_")
#     print("data_parts:", data_parts)
#     subcategory_id = int(data_parts[1])
#     page = int(data_parts[3]) if len(data_parts) > 3 else 1

#     subcategory = await db.get_subcategory(subcategory_id)
#     products = await db.get_all_products(subcategory_id)
#     if not products:
#         await call.message.answer("Товары пока отсутствуют.")
#         return
#     await call.message.answer("Категории пока отсутствуют.")
#     # text = f"*{subcategory.title}*\n\nВыберите товар:"
#     # keyboard = inline_kb.subcategories_kb(products, subcategory_id, page)

#     # await call.message.edit_text(
#     #     text=text,
#     #     reply_markup=keyboard,
#     #     parse_mode="Markdown"
#     # )

@shoping_router.callback_query(F.data.startswith("products_"))
@shoping_router.callback_query(F.data.startswith("subcategory_"))
async def show_products(call: types.CallbackQuery):
    """Обрабатывает нажатие на кнопку подкатегории и выводит товары."""
    subcategory_id = int(call.data.split("_")[-1])

    products = await db.get_all_products(subcategory_id)
    products = list(products)  # Преобразуем QuerySet в список

    if not products:
        await call.message.answer("❌ В этой категории пока нет товаров.")
        return

    page = 1
    # paginated_products, pagination_buttons = paginate_products(products, page, 1, f"product_{subcategory_id}")

    product = products[0]  # Берем первый товар на текущей странице
    caption = f"{hbold(product.title)}\n{hitalic(product.description)}\n💰 Цена: {product.price} р."

    keyboard = inline_kb.product_kb(products, subcategory_id, page)
    # keyboard = InlineKeyboardMarkup(inline_keyboard=[pagination_buttons])
    image_file = FSInputFile(product.image.path)
    await call.message.answer_photo(photo=image_file, caption=caption, reply_markup=keyboard)


@shoping_router.callback_query(F.data.startswith("product_"))
async def paginate_product_handler(call: types.CallbackQuery):
    """Обрабатывает кнопки "Вперед" и "Назад"."""
    data = call.data.split("_")
    subcategory_id = int(data[1])
    page = int(data[-1])

    products = await db.get_all_products(subcategory_id)
    products = list(products)  # Преобразуем QuerySet в список

    paginated_products, pagination_buttons = paginate_products(products, page, 1, f"product_{subcategory_id}")

    product = paginated_products[0]  # Берем товар на текущей странице
    caption = f"{hbold(product.title)}\n{hitalic(product.description)}\n💰 Цена: {product.price} р."

    # keyboard = InlineKeyboardMarkup(row_width=2).add(*pagination_buttons)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[pagination_buttons])
    # keyboard = InlineKeyboardMarkup(inline_keyboard=[pagination_buttons])

    await call.message.edit_caption(caption, reply_markup=keyboard)

    # image_url = product.image.url
    # image_path = os.path.join(settings.MEDIA_ROOT, image_url)
    # image_file = open(image_path, 'rb')

    # keyboard = InlineKeyboardMarkup(inline_keyboard=[pagination_buttons])

    # await call.message.edit_caption(caption, reply_markup=keyboard)
    # await call.message.answer_photo(photo=image_file)
    # image_file.close()
