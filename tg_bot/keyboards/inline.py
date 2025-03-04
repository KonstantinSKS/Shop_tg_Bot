from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tg_bot.config import PAGINATION_ITEMS
from .pagination import paginate_items, paginate_subcategories
from .callback_data import (
    CartCallback, CategoriesCallback, SubcategoryCallback, ProductItemCallback,
    ProductActionCallback, CartItemCallback, BackCallback)


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


def back_to_main_menu():
    """Вазврат в главное меню."""

    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        BUTTON_BACK_MAIN_MENU
    )
    return keyboard.as_markup()


def download_kb() -> InlineKeyboardMarkup:
    """Кнопка «Скачать Excel»."""

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Скачать Excel",
            callback_data=CartCallback(action="download_excel").pack()
        )
    )
    return builder.as_markup()


def main_menu():
    """Главное меню."""

    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text="Перейти в каталог",
            callback_data=CategoriesCallback(level="categories", page=1).pack())
    )
    keyboard.row(
        InlineKeyboardButton(
            text="Корзина 🛒",
            callback_data=CartCallback(action="view").pack())
    )
    keyboard.row(
        InlineKeyboardButton(text="FAQ", callback_data="FAQ")
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
        categories, page, PAGINATION_ITEMS)

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
        subcategories, category_id, page, PAGINATION_ITEMS)

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
            text="В корзину 🛒",
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


def build_cart_message_and_kb(cart):
    """Создает клавиатуру для управления корзиной."""

    keyboard_builder = InlineKeyboardBuilder()
    text = "🛒 *Ваша корзина:*\n\n"
    cart_items = list(cart.cart_products.all())
    if not cart_items:
        text += "В корзине нет товаров."
    else:
        overall_total = 0
        for item in cart_items:
            total_price = item.total_price
            overall_total += total_price
            text += (
                f"• *{item.product.title}*\n"
                f"  Кол-во: {item.quantity} | Цена: {item.product.price} р. | Сумма: {total_price} р.\n\n"
            )
            keyboard_builder.row(
                InlineKeyboardButton(
                    text="➖",
                    callback_data=CartItemCallback(product_id=item.product.id, action="decrease").pack()
                ),
                InlineKeyboardButton(
                    text=f"❌ {item.product.title}",
                    callback_data=CartItemCallback(product_id=item.product.id, action="remove").pack()
                ),
                InlineKeyboardButton(
                    text="➕",
                    callback_data=CartItemCallback(product_id=item.product.id, action="increase").pack()
                )
            )
        text += f"*Общая сумма:* {overall_total} р.\n\n"

    keyboard_builder.row(
        InlineKeyboardButton(
            text="Оформить заказ",
            callback_data=CartCallback(action="checkout").pack()),
        BUTTON_BACK_MAIN_MENU
    )
    return text, keyboard_builder.as_markup()


def delivery_kb() -> InlineKeyboardMarkup:
    """Возвращает клавиатуру для подтверждения адреса доставки."""

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Перейти к оплате",
            callback_data=CartCallback(action="proceed_to_payment").pack())],
        [
            InlineKeyboardButton(
                text="Назад",
                callback_data=CartCallback(action="back_to_address").pack()
            ),
            BUTTON_BACK_MAIN_MENU
        ]
    ])
    return keyboard
