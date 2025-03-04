from aiogram.fsm.context import FSMContext
from aiogram import types, Router, F

from tg_bot.config import PROVIDER_TOKEN
from tg_bot.db import db_commands as db
from tg_bot.loader import bot
from tg_bot.misc.utils import generate_order_excel
from tg_bot.settings_logger import logger
from tg_bot.states.all_states import StateShop, OrderStates
from tg_bot.keyboards import inline as inline_kb
from tg_bot.keyboards.callback_data import (
    CartCallback, ProductActionCallback, CartItemCallback)


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
                logger.error(f"{Exception} Функция удаления сообщения не сработала.")
                pass

        confirm_msg_id = data.get("confirm_msg_id")
        if confirm_msg_id:
            try:
                await call.message.bot.delete_message(call.message.chat.id, confirm_msg_id)
            except Exception:
                logger.error(f"{Exception} Функция удаления сообщения не сработала.")
                pass

        tg_user = await db.get_tg_user(call.from_user.id)
        await db.create_or_add_to_cart(tg_user, [{'id': product.id, 'quantity': quantity}])
        logger.info(f"Пользователь {call.from_user.full_name} добавл в корзину товар {product.title}: {quantity} шт.")
        await call.answer(f"Товар добавлен в корзину в количестве: {quantity}", show_alert=True)
        await state.clear()

    elif callback_data.action == "confirm":
        tg_user = await db.get_tg_user(call.from_user.id)
        cart = await db.get_cart(tg_user)
        if not cart or not cart.cart_products.exists():
            await call.answer("Ваша корзина пуста", show_alert=True)
            logger.info(f"Корзина пользователя {call.from_user.full_name} пустая.")
            return
        text, cart_kb = inline_kb.build_cart_message_and_kb(cart)

        try:
            await call.message.delete()
        except Exception:
            logger.error(f"{Exception} Функция удаления сообщения не сработала.")
            pass

        await bot.send_message(call.message.chat.id, text, reply_markup=cart_kb, parse_mode="Markdown")
        await state.clear()
        await call.answer()


@shopping_cart_router.message(StateShop.set_quantity)
async def process_quantity_input(message: types.Message, state: FSMContext):
    """Обрабатывает введённое количество товара.
    Валидирует введенное значение --> int."""

    try:
        quantity = int(message.text)
        if quantity < 1:
            logger.info(f"{ValueError}, Пользователь ввел неправильное число {quantity}")
            raise ValueError("Количество должно быть не менее 1")
    except ValueError:
        logger.info(f"{ValueError}, Пользователь ввел неправильное число, либо строку")
        await message.answer("Пожалуйста, введите целое число больше нуля.")
        return
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        await message.answer("Произошла ошибка. Попробуйте ещё раз.")
        return

    await state.update_data(quantity=quantity)
    try:
        await message.delete()
    except Exception:
        logger.error(f"{Exception} Функция удаления сообщения не сработала.")
        pass

    confirm_msg = await message.answer(f"Количество: {quantity}. Для продолжения нажмите «Добавить в корзину».")
    await state.update_data(confirm_msg_id=confirm_msg.message_id)


@shopping_cart_router.callback_query(CartItemCallback.filter())
async def cart_item_handler(
        call: types.CallbackQuery,
        callback_data: CartItemCallback):
    """Обрабатывает действия с товарами в корзине."""

    tg_user = await db.get_tg_user(call.from_user.id)
    cart = await db.get_cart(tg_user)
    if not cart:
        await call.answer("Корзина не найдена", show_alert=True)
        logger.warning("Корзина не найдена!")
        return

    try:
        cart_item = cart.cart_products.get(product_id=callback_data.product_id)
    except Exception:
        await call.answer("Товар не найден в корзине")
        logger.warning("Товар не найден в корзине!")
        return

    if callback_data.action == "decrease":
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            await call.answer("Минимальное количество - 1", show_alert=True)
    elif callback_data.action == "increase":
        cart_item.quantity += 1
        cart_item.save()
    elif callback_data.action == "remove":
        cart_item.delete()

    text, cart_kb = inline_kb.build_cart_message_and_kb(cart)
    try:
        await call.message.edit_text(text, reply_markup=cart_kb, parse_mode="Markdown")
    except Exception:
        await call.message.answer(text, reply_markup=cart_kb, parse_mode="Markdown")
    await call.answer()


@shopping_cart_router.callback_query(CartCallback.filter(F.action == "view"))
async def view_cart_handler(call: types.CallbackQuery, callback_data: CartCallback):
    """Переход в корзину из главного меню."""

    tg_user = await db.get_tg_user(call.from_user.id)
    cart = await db.get_cart(tg_user)
    if not cart or not cart.cart_products.exists():
        await call.answer("Ваша корзина пуста", show_alert=True)
        logger.warning(f"Корзина пользователя {call.from_user.full_name} пустая!")
        return

    text, cart_kb = inline_kb.build_cart_message_and_kb(cart)
    try:
        await call.message.edit_text(text, reply_markup=cart_kb, parse_mode="Markdown")
    except Exception:
        await call.message.answer(text, reply_markup=cart_kb, parse_mode="Markdown")
    await call.answer()


@shopping_cart_router.callback_query(CartCallback.filter(F.action == "checkout"))
async def checkout_handler(
        call: types.CallbackQuery,
        callback_data: CartCallback,
        state: FSMContext):
    """Обрабатывает нажатие кнопки «Оформить заказ».
    Запрашивает у пользователя ввод адреса доставки."""

    await call.message.edit_text("Введите ваш адрес доставки:")
    await state.set_state(OrderStates.waiting_for_address)
    await call.answer()


@shopping_cart_router.message(OrderStates.waiting_for_address)
async def process_delivery_address(message: types.Message, state: FSMContext):
    """Обрабатывает введённый адрес доставки и выводит кнопку «Перейти к оплате»."""

    address = message.text.strip()
    if not address:
        await message.answer("Адрес не может быть пустым. Пожалуйста, введите корректный адрес доставки.")
        return

    tg_user = await db.get_tg_user(message.from_user.id)
    if not tg_user:
        await message.answer("Пользователь не найден.")
        await state.clear()
        return
    await db.create_delivery_address(tg_user, address)
    logger.info(f"Пользователь {message.from_user.full_name} ввел адрес {address}")

    keyboard = inline_kb.delivery_kb()
    await message.answer("Адрес доставки успешно сохранён.", reply_markup=keyboard)
    await state.clear()


@shopping_cart_router.callback_query(CartCallback.filter(F.action == "back_to_address"))
async def back_to_address_handler(call: types.CallbackQuery, callback_data: CartCallback, state: FSMContext):
    """Возвращает пользователя к вводу адреса доставки."""

    await call.message.edit_text("Введите ваш адрес доставки:")
    await state.set_state(OrderStates.waiting_for_address)
    await call.answer()


@shopping_cart_router.callback_query(CartCallback.filter(F.action == "proceed_to_payment"))
async def proceed_to_payment_handler(
        call: types.CallbackQuery,
        callback_data: CartCallback,
        state: FSMContext):

    tg_user = await db.get_tg_user(call.from_user.id)
    cart = await db.get_cart(tg_user)
    cart_items = cart.cart_products.all()

    prices = list()
    for item in cart_items:
        prices.append(types.LabeledPrice(
            label=f"{item.product.title} : {item.quantity}",
            amount=int(item.total_price * 100)
        ))
    logger.info(f"Пользователь {call.from_user.full_name} отправил на оплату следующие позиции:{prices}")

    kb = inline_kb.download_kb()

    await bot.send_invoice(
        chat_id=call.from_user.id,
        title=f"заказ № {cart.id}",
        description=" Оплата покупок.",
        payload=f"Test order #{cart.id}",
        provider_token=PROVIDER_TOKEN,
        currency="RUB",
        start_parameter="test",
        prices=prices,
        )

    await call.message.answer("Вы можете скачать данные заказа:", reply_markup=kb)
    await call.answer()


@shopping_cart_router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    """стандартный код для обработки апдейта типа PreCheckoutQuery."""

    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@shopping_cart_router.message(F.successful_payment)
async def process_successful_payment(message: types.Message, state: FSMContext):
    """Стандартный код для обработки успешного платежа."""

    main_menu_kb = inline_kb.back_to_main_menu()
    await message.reply(f"Платеж на сумму {message.successful_payment.total_amount // 100} "
                        f"{message.successful_payment.currency} прошел успешно!",
                        reply_markup=main_menu_kb)
    logger.info(f"Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно!")
    await state.clear()


@shopping_cart_router.callback_query(CartCallback.filter(F.action == "download_excel"))
async def download_excel_handler(call: types.CallbackQuery, callback_data: CartCallback):
    """Обрабатывает нажатие кнопки «Скачать Excel» на этапе оплаты.
    Генерирует Excel‑файл с данными заказа и отправляет его пользователю."""

    tg_user = await db.get_tg_user(call.from_user.id)
    cart = await db.get_cart(tg_user)
    cart_items = cart.cart_products.all()

    order_items = []
    overall_total = 0.0
    for item in cart_items:
        total_price = float(item.total_price)
        overall_total += total_price
        order_items.append({
            'title': item.product.title,
            'quantity': item.quantity,
            'total_price': total_price
        })

    excel_file = generate_order_excel(order_items, overall_total)

    await call.message.answer_document(
        document=excel_file,
        caption="Скачайте Excel‑файл с данными заказа."
    )
    await call.answer()
