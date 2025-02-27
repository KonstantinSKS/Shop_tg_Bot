from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


BUTTON_BACK_MAIN_MENU = InlineKeyboardButton(
    text="Меню 📋", callback_data="back_main_menu"
)


def main_menu():
    """Главное меню."""

    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="Выбрать каталог", callback_data="select_catalog")
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
