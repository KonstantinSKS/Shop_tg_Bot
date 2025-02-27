from aiogram.fsm.context import FSMContext
from aiogram import types, Router, F
from aiogram.filters import Command

from tg_bot.db import db_commands as db
from tg_bot.loader import bot
from tg_bot.settings_logger import logger
from tg_bot.states.all_states import StateUser
from tg_bot.keyboards import inline as inline_kb
from tg_bot.misc.utils import check_sub_channel
from tg_bot.misc import constants as const


base_reg_router = Router()


@base_reg_router.message(Command("help"))
async def command_help(message: types.Message):
    """Обработка команды /help."""

    await message.answer(const.HELP_TEXT)


@base_reg_router.callback_query(F.data == "back_main_menu")
async def back_main_menu(call: types.CallbackQuery, state: FSMContext):
    """Возращение в главное меню."""

    await call.message.delete()
    await main_menu(call.from_user, state)


async def main_menu(user: types.User, state: FSMContext):
    """Главное меню."""

    tg_user = await db.get_tg_user(user.id)

    if not tg_user:
        await bot.send_message(
            chat_id=user.id,
            text=const.NOT_SUB_MESSAGE,
            reply_markup=inline_kb.channels_kb(const.CHANNEL_URL)
        )
        return

    await state.clear()
    await bot.send_message(
        chat_id=user.id,
        text="Главное меню",
        reply_markup=inline_kb.main_menu(),
    )


@base_reg_router.message(Command("start"))
async def command_start(message: types.Message, state: FSMContext):
    """Команда /start, проверка на подписку."""

    logger.info(
        f"Пользователь {message.from_user.full_name} ввел(a) команду /start"
    )
    if check_sub_channel(
        await bot.get_chat_member(
            chat_id=const.CHANNEl_ID, user_id=message.from_user.id)):
        await message.answer(
            text=f"Здравствуйте, {message.from_user.first_name}! 😊"
        )
        await main_menu(message.from_user, state)
    else:
        await message.answer(
            const.NOT_SUB_MESSAGE,
            reply_markup=inline_kb.channels_kb(const.CHANNEL_URL))


@base_reg_router.callback_query(F.data == "sub_channel_done")
async def sub_channel_done(call: types.CallbackQuery, state: FSMContext):
    """Удаляет кнопку "Подписаться", если пользователь подписался,
    создает учетную запись пользователя и перенаправляет в основное меню.
    """

    await bot.delete_message(call.from_user.id, call.message.message_id)
    if check_sub_channel(
        await bot.get_chat_member(
            chat_id=const.CHANNEl_ID, user_id=call.from_user.id)):
        if not await db.tg_user_exists(call.from_user.id):
            await db.create_tg_user(
                user=call.from_user,
                is_subscribed=True
            )
        await call.message.answer(
            text=f"Здравствуйте, {call.from_user.first_name}! 😊"
        )
        await main_menu(call.from_user, state)
    else:
        await call.message.answer(
            const.NOT_SUB_MESSAGE,
            reply_markup=inline_kb.channels_kb(const.CHANNEL_URL))
