from aiogram.filters.callback_data import CallbackData


class CategoriesCallback(CallbackData, prefix="categories"):
    page: int
    level: str


class SubcategoryCallback(CallbackData, prefix="subcategories"):
    category_id: int
    page: int
    level: str


class ProductCallback(CallbackData, prefix="product"):
    subcategory_id: int
    page: int


class ProductItemCallback(CallbackData, prefix="product_item"):
    subcategory_id: int
    product_index: int


class ProductActionCallback(CallbackData, prefix="product_action"):
    subcategory_id: int
    product_index: int
    action: str


class CartItemCallback(CallbackData, prefix="cart_item"):
    product_id: int
    action: str


class CartCallback(CallbackData, prefix="cart"):
    action: str


class BackCallback(CallbackData, prefix="back_step"):
    level: str
