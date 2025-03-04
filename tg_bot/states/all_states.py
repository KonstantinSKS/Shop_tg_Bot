from aiogram.fsm.state import StatesGroup, State


class StateShop(StatesGroup):
    browsing = State()
    subcategory_selected = State()
    product_view = State()
    ordering = State()
    set_quantity = State()


class OrderStates(StatesGroup):
    waiting_for_delivery_info = State()
    waiting_for_payment = State()
    waiting_for_address = State()


class StateUser(StatesGroup):
    faq: State = State()
