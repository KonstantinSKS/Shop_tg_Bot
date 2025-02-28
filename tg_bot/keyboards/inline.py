from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tg_bot.misc import constants as const
from .pagination import paginate_items

from math import ceil

BUTTON_BACK_MAIN_MENU = InlineKeyboardButton(
    text="В главное Меню 📋", callback_data="back_main_menu"
)
BUTTONS_BACK_STEP = InlineKeyboardButton(
    text="Назад ↩️", callback_data="back_step"
)


def main_menu():
    """Главное меню."""

    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="Перейти в каталог", callback_data="catalog")
    )
    keyboard.row(
        InlineKeyboardButton(text="Корзина 🛒", callback_data="shopping_cart")
    )
    keyboard.row(
        InlineKeyboardButton(text="FAQ", callback_data="faq")
    )
    return keyboard.as_markup()


def back_main_menu():
    """Вернуться в главное меню."""

    keyboard = InlineKeyboardBuilder()
    keyboard.add(BUTTON_BACK_MAIN_MENU)
    return keyboard.as_markup()


def back_step():
    """Вернуться на шаг назад и вернуться в главное меню."""

    keyboard = builder_back_step_and_main_menu()
    return keyboard.as_markup()


def builder_back_step_and_main_menu():
    """Builder для кнопок Назад и Меню."""

    keyboard = InlineKeyboardBuilder()
    keyboard.add(BUTTONS_BACK_STEP)
    keyboard.add(BUTTON_BACK_MAIN_MENU)
    return keyboard.adjust(1)


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
        categories, page, const.PAGINATION_ITEMS, "categories")

    for category in paginated_categories:
        builder.button(
            text=category.title,
            callback_data=f"category_{category.id}"
        )

    if pagination_buttons:
        builder.row(*pagination_buttons)

    builder.add(BUTTON_BACK_MAIN_MENU)
    return builder.as_markup()


def subcategories_kb(subcategories, category_id, page=1):
    """Создает клавиатуру с подкатегориями и кнопками управления."""

    builder = InlineKeyboardBuilder()
    paginated_subcategories, pagination_buttons = paginate_items(
        subcategories, page, const.PAGINATION_ITEMS, f"category_{category_id}")

    for subcategory in paginated_subcategories:
        builder.button(
            text=subcategory.title,
            callback_data=f"subcategory_{subcategory.id}"
        )

    if pagination_buttons:
        builder.row(*pagination_buttons)

    builder.row(BUTTONS_BACK_STEP, BUTTON_BACK_MAIN_MENU)
    return builder.as_markup()

def product_kb(products, products_id, page=1):
    """Создает клавиатуру с товарами и кнопками управления."""

    builder = InlineKeyboardBuilder()
    paginated_products, pagination_buttons = paginate_items(
        products, page, const.PAGINATION_ITEMS, f"products_{products_id}")

    for subcategory in paginated_products:
        builder.button(
            text=subcategory.title,
            callback_data=f"subcategory_{subcategory.id}"
        )

    if pagination_buttons:
        builder.row(*pagination_buttons)

    builder.row(BUTTONS_BACK_STEP, BUTTON_BACK_MAIN_MENU)
    return builder.as_markup()
