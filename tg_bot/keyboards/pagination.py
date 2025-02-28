from aiogram.types import InlineKeyboardButton


def paginate_items(items, page, per_page, callback_prefix):
    """Функция для пагинации списка элементов и генерации кнопок навигации."""

    total_pages = (len(items) + per_page - 1) // per_page
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_items = items[start_idx:end_idx]

    pagination_buttons = []
    if page > 1:
        pagination_buttons.append(InlineKeyboardButton(
            text="⬅ Назад", callback_data=f"{callback_prefix}_page_{page - 1}"))
    if page < total_pages:
        pagination_buttons.append(InlineKeyboardButton(
            text="Вперед ➡", callback_data=f"{callback_prefix}_page_{page + 1}"))

    return paginated_items, pagination_buttons
