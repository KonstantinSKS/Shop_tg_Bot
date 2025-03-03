from enum import IntEnum, auto
from typing import Optional

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


class ProductAction(IntEnum):
    details = auto()


class BackCallback(CallbackData, prefix="back_step"):
    level: str  # уровень (например, "catalog", "category", "subcategory")
    # category_id: int = None  # ID категории (если есть)
    # subcategory_id: int = None  # ID подкатегории (если есть)
    # page: int = 1
