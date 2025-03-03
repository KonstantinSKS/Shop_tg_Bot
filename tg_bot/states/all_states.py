from aiogram.fsm.state import StatesGroup, State


class StateShop(StatesGroup):
    browsing = State()               # Пользователь просматривает категории
    subcategory_selected = State()   # Пользователь выбрал категорию, просматривает подкатегории
    product_view = State()           # Пользователь просматривает товар
    ordering = State()
    set_quantity = State()

    # subcategories = State()
