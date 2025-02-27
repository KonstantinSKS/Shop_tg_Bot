from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def imei_keyboard():
    """Reply-клавиша для отправки IMEI."""

    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Отправить IMEI")]],
        resize_keyboard=True,
    )
