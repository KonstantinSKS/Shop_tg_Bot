from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tg_bot.misc import constants as const


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


def create_categories_kb(categories, page=0):
    """Создает инлайн-клавиатуру с категориями и пагинацией."""

    builder = InlineKeyboardBuilder()
    start_idx = page * const.CATEGORIES_PER_PAGE
    end_idx = start_idx + const.CATEGORIES_PER_PAGE

    # Добавляем категории в кнопки
    for category in categories[start_idx:end_idx]:
        builder.button(
            text=category.title,
            callback_data=f"category_{category.id}"
        )

    # Кнопки "Назад" и "Вперед"
    buttons = []
    if page > 0:
        buttons.append(InlineKeyboardButton(
            text="⬅ Назад", callback_data=f"categories_page_{page - 1}"))
    if end_idx < len(categories):
        buttons.append(InlineKeyboardButton(
            text="Вперед ➡", callback_data=f"categories_page_{page + 1}"))

    # Добавляем навигационные кнопки в новую строку
    if buttons:
        builder.row(*buttons)

    builder.add(BUTTON_BACK_MAIN_MENU)

    return builder.adjust(2).as_markup()
