from aiogram.filters.callback_data import CallbackData


class CategoriesCallback(CallbackData, prefix="categories"):
    page: int
    level: str


class SubcategoryCallback(CallbackData, prefix="subcategories"):
    category_id: int
    page: int
    level: str


class BackCallback(CallbackData, prefix="back_step"):
    level: str  # уровень (например, "catalog", "category", "subcategory")
    # category_id: int = None  # ID категории (если есть)
    # subcategory_id: int = None  # ID подкатегории (если есть)
    # page: int = 1


# class ProductCallback(CallbackData, prefix="product"):
