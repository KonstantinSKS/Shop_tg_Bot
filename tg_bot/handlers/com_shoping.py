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
from tg_bot.keyboards.callback_data import CategoriesCallback, SubcategoryCallback, BackCallback
from tg_bot.misc.utils import check_sub_channel
from tg_bot.misc import constants as const
from tg_bot.keyboards.pagination import paginate_products


shoping_router = Router()


@shoping_router.callback_query(CategoriesCallback.filter())  # F.level == "categories"
async def get_categories(call: types.CallbackQuery, callback_data: CategoriesCallback):
    """Получение всех категорий товаров с пагинацией."""

    categories = await db.get_all_categories()
    if not categories:
        await call.message.answer("Категории пока отсутствуют.") # cache_time=3
        return

    await call.message.edit_text(
        "Выберите категорию:",
        reply_markup=inline_kb.categories_kb(categories, callback_data.page)
    )


# @shoping_router.callback_query(BackCallback.filter(F.level == "subcategory"))
@shoping_router.callback_query(SubcategoryCallback.filter())  # F.level == "categories"
async def show_category(call: types.CallbackQuery, callback_data: SubcategoryCallback):
    """Отображает категорию и список её подкатегорий с пагинацией."""

    category = await db.get_category(callback_data.category_id)
    subcategories = await db.get_all_subcategories(callback_data.category_id)
    if not subcategories:
        await call.message.answer("Подкатегории пока отсутствуют.") #cache_time=3
        return

    text = f"*{category.title}*\n\nВыберите подкатегорию:"
    keyboard = inline_kb.subcategories_kb(subcategories, callback_data.category_id, callback_data.page)

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

# @shoping_router.callback_query(F.data.startswith("products_"))
# @shoping_router.callback_query(F.data.startswith("subcategory_"))
# async def show_products(call: types.CallbackQuery):
#     """Обрабатывает нажатие на кнопку подкатегории и выводит товары."""
#     print("call.data:", call.data)
#     subcategory_id = int(call.data.split("_")[-1])
#     print("subcategory_id:", subcategory_id)

#     products = await db.get_all_products(subcategory_id)
#     # products = list(products)  # Преобразуем QuerySet в список

#     if not products:
#         await call.message.answer("❌ В этой категории пока нет товаров.")
#         return

#     page = 1
#     # paginated_products, pagination_buttons = paginate_products(products, page, 1, f"product_{subcategory_id}")
#     # for product in products:

#     product = products[0]  # Берем первый товар на текущей странице
#     caption = f"{hbold(product.title)}\n{hitalic(product.description)}\n💰 Цена: {product.price} р."

#     keyboard = inline_kb.product_kb(product, page)  # subcategory_id
#     # keyboard = InlineKeyboardMarkup(inline_keyboard=[pagination_buttons])
#     image_file = FSInputFile(product.image.path)
#     await call.message.answer_photo(photo=image_file, caption=caption, reply_markup=keyboard)


@shoping_router.callback_query(F.data.startswith("products_"))
@shoping_router.callback_query(F.data.startswith("subcategory_"))
async def show_products(call: types.CallbackQuery):
    """Обрабатывает нажатие на кнопку подкатегории и выводит товары."""
    print("call.data:", call.data)

    data_parts = call.data.split("_")

    if len(data_parts) == 2:  # Нажатие на подкатегорию
        subcategory_id = int(data_parts[1])
        page = 1  # Начинаем с первой страницы
    elif len(data_parts) == 4:  # Нажатие на кнопку "вперед" или "назад"
        subcategory_id = int(data_parts[1])
        page = int(data_parts[3])  # Получаем новую страницу
    else:
        print("Ошибка в callback_data:", call.data)
        return

    print(f"subcategory_id: {subcategory_id}, page: {page}")

    products = await db.get_all_products(subcategory_id)
    if not products:
        await call.message.answer("❌ В этой категории пока нет товаров.")
        return

    if page < 1 or page > len(products):
        return  # Предотвращаем выход за границы списка

    product = products[page - 1]  # Выбираем нужный товар
    caption = f"{hbold(product.title)}\n{hitalic(product.description)}\n💰 Цена: {product.price} р."

    keyboard = inline_kb.product_kb(product.id, subcategory_id, page)
    image_file = FSInputFile(product.image.path)

    await call.message.edit_media(
        types.InputMediaPhoto(media=image_file, caption=caption),
        reply_markup=keyboard
    )


@shoping_router.callback_query(F.data.startswith("subcategory_"))
async def show_products(call: types.CallbackQuery):
    """Обрабатывает нажатие на кнопку подкатегории и выводит товары."""