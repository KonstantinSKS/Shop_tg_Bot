import hashlib
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from tg_bot.misc.constants import FAQ_LIST
from tg_bot.loader import bot
from tg_bot.states.all_states import StateUser


faq_router = Router()


@faq_router.callback_query(F.data == "FAQ")
async def faq_callback_handler(call: types.CallbackQuery, state: FSMContext):
    """Переводит пользователя в режим FAQ при нажатии на кнопку FAQ."""

    await state.set_state(StateUser.faq)
    bot_username = (await bot.get_me()).username
    text = f"Вы в разделе FAQ.\nВведите <code>@{bot_username}</code> и после начните вводить ваш вопрос."

    await call.message.answer(text)


@faq_router.inline_query(StateUser.faq)
async def process_faq_inline(query: types.InlineQuery):
    """
    Обрабатывает inline-запросы, когда пользователь находится в состоянии FAQ.
    Автоматически подбирает вопросы из faq_list, содержащие введённую подстроку.
    """
    results = []
    query_text = query.query.lower()
    for question, answer in FAQ_LIST.items():
        if query_text in question.lower():
            results.append(
                types.InlineQueryResultArticle(
                    id=hashlib.md5(question.encode()).hexdigest(),
                    title=question,
                    input_message_content=types.InputTextMessageContent(message_text=answer)
                )
            )
    await query.answer(results=results, cache_time=1)
