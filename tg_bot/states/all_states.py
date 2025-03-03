from aiogram.fsm.state import StatesGroup, State


class StateShop(StatesGroup):
    subcategories = State()
