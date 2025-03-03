from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tg_bot.misc import constants as const
from .pagination import paginate_items, paginate_subcategories
from .callback_data import (
    CategoriesCallback, SubcategoryCallback, ProductItemCallback,
    ProductActionCallback, BackCallback)


BUTTON_BACK_MAIN_MENU = InlineKeyboardButton(
    text="В главное Меню 📋", callback_data="back_main_menu"
)
BUTTONS_BACK_STEP = InlineKeyboardButton(
    text="Назад ↩️", callback_data="back_step"
)


def button_back_step(level: str) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text="Назад ↩️",
        callback_data=BackCallback(level=level).pack()
    )


def main_menu():
    """Главное меню."""

    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text="Перейти в каталог",
            callback_data=CategoriesCallback(level="categories", page=1).pack())
    )
    keyboard.row(
        InlineKeyboardButton(text="Корзина 🛒", callback_data="shopping_cart")
    )
    keyboard.row(
        InlineKeyboardButton(text="FAQ", callback_data="faq")
    )
    return keyboard.as_markup()


def channels_kb(channel_url: str):
    """Подписаться на канал."""

    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="Подписаться 🔔", url=channel_url)
    )
    keyboard.row(
        InlineKeyboardButton(text="Подписался", callback_data="sub_channel_done")
    )
    return keyboard.as_markup()


def categories_kb(categories, page=1):
    """Создает инлайн-клавиатуру с категориями и пагинацией."""

    builder = InlineKeyboardBuilder()
    paginated_categories, pagination_buttons = paginate_items(
        categories, page, const.PAGINATION_ITEMS)

    for category in paginated_categories:
        builder.button(
            text=category.title,
            callback_data=SubcategoryCallback(
                category_id=category.id, page=1, level="subcategories").pack()
        )

    if pagination_buttons:
        builder.row(*pagination_buttons)

    builder.add(BUTTON_BACK_MAIN_MENU)
    return builder.as_markup()


def subcategories_kb(subcategories, category_id, page=1):
    """Создает клавиатуру с подкатегориями и кнопками управления."""

    builder = InlineKeyboardBuilder()
    paginated_subcategories, pagination_buttons = paginate_subcategories(
        subcategories, category_id, page, const.PAGINATION_ITEMS)

    for subcategory in paginated_subcategories:
        builder.button(
            text=subcategory.title,
            callback_data=ProductItemCallback(
                subcategory_id=subcategory.id,
                product_index=1
            ).pack()
        )

    if pagination_buttons:
        builder.row(*pagination_buttons)

    BACK_BUTTON = InlineKeyboardButton(
        text="↩️ В предыдущий раздел",
        callback_data=CategoriesCallback(level="categories", page=1).pack()
    )

    builder.row(BACK_BUTTON, BUTTON_BACK_MAIN_MENU)
    return builder.as_markup()


def product_item_kb(subcategory_id, product_index, total_products, category_id):
    """Создает клавиатуру для навигации по товарам в подкатегории."""

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Добавить в корзину",
            callback_data=ProductActionCallback(
                subcategory_id=subcategory_id,
                product_index=product_index,
                action="add"
            ).pack()
        ),
        InlineKeyboardButton(
            text="Указать кол-во",
            callback_data=ProductActionCallback(
                subcategory_id=subcategory_id,
                product_index=product_index,
                action="set_quantity"
            ).pack()
        ),
        InlineKeyboardButton(
            text="Подтвердить",
            callback_data=ProductActionCallback(
                subcategory_id=subcategory_id,
                product_index=product_index,
                action="confirm"
            ).pack()
        )
    )

    pagination_buttons = []
    if product_index > 1:
        pagination_buttons.append(
            InlineKeyboardButton(
                text="⬅ Назад",
                callback_data=ProductItemCallback(
                    subcategory_id=subcategory_id,
                    product_index=product_index - 1
                ).pack()
            )
        )
    if product_index < total_products:
        pagination_buttons.append(
            InlineKeyboardButton(
                text="Вперед ➡",
                callback_data=ProductItemCallback(
                    subcategory_id=subcategory_id,
                    product_index=product_index + 1
                ).pack()
            )
        )
    if pagination_buttons:
        builder.row(*pagination_buttons)

    builder.row(
        InlineKeyboardButton(
            text="↩️ В предыдущий раздел",
            callback_data=SubcategoryCallback(
                category_id=category_id,
                page=1,
                level="subcategories").pack()
        ),
        BUTTON_BACK_MAIN_MENU
    )

    return builder.as_markup()
