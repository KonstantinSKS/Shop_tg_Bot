from aiogram.types import InlineKeyboardButton

from .callback_data import CategoriesCallback, SubcategoryCallback, ProductCallback


def paginate_items(items, page, per_page):
    """Функция для пагинации списка элементов и генерации кнопок навигации."""

    total_pages = (len(items) + per_page - 1) // per_page
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_items = items[start_idx:end_idx]

    pagination_buttons = []
    if page > 1:
        pagination_buttons.append(InlineKeyboardButton(
            text="⬅ Назад",
            # callback_data=f"{callback_prefix}_page_{page - 1}")
            callback_data=CategoriesCallback(page=page - 1, level="categories").pack())
        )
    if page < total_pages:
        pagination_buttons.append(InlineKeyboardButton(
            text="Вперед ➡",
            # callback_data=f"{callback_prefix}_page_{page + 1}")
            callback_data=CategoriesCallback(page=page + 1, level="categories").pack())
        )

    return paginated_items, pagination_buttons


def paginate_subcategories(subcategories, category_id, page, per_page):
    """Функция для пагинации списка подкатегорий и генерации кнопок навигации."""

    total_pages = (len(subcategories) + per_page - 1) // per_page
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_subcategories = subcategories[start_idx:end_idx]

    pagination_buttons = []
    if page > 1:
        pagination_buttons.append(InlineKeyboardButton(
            text="⬅ Назад",
            callback_data=SubcategoryCallback(category_id=category_id, page=page - 1, level="subcategories").pack()
        ))
    if page < total_pages:
        pagination_buttons.append(InlineKeyboardButton(
            text="Вперед ➡",
            callback_data=SubcategoryCallback(category_id=category_id, page=page + 1, level="subcategories").pack()
        ))

    return paginated_subcategories, pagination_buttons


def paginate_products(products, subcategory_id, page):  # products, per_page,
    """Функция для пагинации списка товаров и генерации кнопок навигации."""
    # total_pages = (len(products) + per_page - 1) // per_page
    # start_idx = (page - 1) * per_page
    # end_idx = start_idx + per_page
    # paginated_products = products[start_idx:end_idx]

    start_idx = (page - 1)
    end_idx = start_idx + 1
    paginated_products = products[start_idx:end_idx]

    print("page:", page)
    pagination_buttons = []
    # if page > 1:
    pagination_buttons.append(InlineKeyboardButton(
        text="⬅ Назад",
        # callback_data=f"{callback_prefix}_page_{page - 1}")
        callback_data=ProductCallback(subcategory_id=subcategory_id, page=page - 1).pack()
    ))
    # print("назад callback_prefix и page:", callback_prefix, page)
    # if page < total_pages:
    pagination_buttons.append(InlineKeyboardButton(
        text="Вперед ➡",
        # callback_data=f"{callback_prefix}_page_{page + 1}")
        callback_data=ProductCallback(subcategory_id=subcategory_id, page=page + 1).pack()
    ))
    # print("вперед callback_prefix и page:", callback_prefix, page)

    return pagination_buttons, paginated_products
