from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hbold, hitalic
# from aiogram.types import InlineKeyboardMarkup
from aiogram import types, Router, F
# from aiogram.filters import Command
# from aiogram.exceptions import TelegramBadRequest

from tg_bot.db import db_commands as db
# from tg_bot.loader import bot
# from tg_bot.settings_logger import logger
from tg_bot.states.all_states import StateShop
from tg_bot.keyboards import inline as inline_kb
from tg_bot.keyboards.callback_data import (
    ProductActionCallback, ProductItemCallback, SubcategoryCallback, ProductCallback)
# from tg_bot.misc.utils import check_sub_channel
# from tg_bot.misc import constants as const


shopping_cart_router = Router()


@shopping_cart_router.callback_query(ProductActionCallback.filter())
async def add_product_to_cart(
        call: types.CallbackQuery,
        callback_data: ProductActionCallback,
        state: FSMContext):
    """Добавляет товар в корзину."""

    products = await db.get_all_products(callback_data.subcategory_id)
    products = list(products)
    product = products[callback_data.product_index - 1]

    if callback_data.action == "set_quantity":
        await state.update_data(
            product_id=product.id,
            subcategory_id=callback_data.subcategory_id,
            product_index=callback_data.product_index
        )
        await state.set_state(StateShop.set_quantity)
        quantity_msg = await call.message.answer("Введите желаемое количество товара (числом):")
        await state.update_data(quantity_msg_id=quantity_msg.message_id)
        await call.answer()

    elif callback_data.action == "add":
        data = await state.get_data()

        if data.get("product_id") == product.id and "quantity" in data:
            quantity = data["quantity"]
        else:
            quantity = 1

        quantity_msg_id = data.get("quantity_msg_id")
        if quantity_msg_id:
            try:
                await call.message.bot.delete_message(call.message.chat.id, quantity_msg_id)
            except Exception:
                pass

        confirm_msg_id = data.get("confirm_msg_id")
        if confirm_msg_id:
            try:
                await call.message.bot.delete_message(call.message.chat.id, confirm_msg_id)
            except Exception:
                pass

        tg_user = await db.get_tg_user(call.from_user.id)
        await db.create_or_add_to_cart(tg_user, [{'id': product.id, 'quantity': quantity}])
        await call.answer(f"Товар добавлен в корзину в количестве: {quantity}", show_alert=True)
        await state.clear()

    elif callback_data.action == "confirm":
        await call.answer("Подтверждение пока не реализовано", show_alert=True)
    else:
        await call.answer("Неизвестное действие", show_alert=True)


@shopping_cart_router.message(StateShop.set_quantity)
async def process_quantity_input(message: types.Message, state: FSMContext):
    """
    Обрабатывает введённое количество товара.
    Валидирует введенное значение --> int."""

    try:
        quantity = int(message.text)
        if quantity < 1:
            raise ValueError("Количество должно быть не менее 1")
    except ValueError:
        await message.answer("Пожалуйста, введите целое число больше нуля.")
        return

    await state.update_data(quantity=quantity)
    try:
        await message.delete()
    except Exception:
        pass

    confirm_msg = await message.answer(f"Количество: {quantity}. Для продолжения нажмите «Добавить в корзину».")
    await state.update_data(confirm_msg_id=confirm_msg.message_id)
