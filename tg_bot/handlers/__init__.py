from tg_bot.handlers.base_com_registration import base_reg_router
from tg_bot.handlers.com_shoping import shoping_router
from tg_bot.handlers.com_shopping_cart import shopping_cart_router
from tg_bot.handlers.com_faq import faq_router

all_handlers = (
    base_reg_router,
    shoping_router,
    shopping_cart_router,
    faq_router,
)
