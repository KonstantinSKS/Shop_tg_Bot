import openpyxl
from io import BytesIO
from aiogram.types import InputFile
from aiogram.types.input_file import BufferedInputFile


def check_sub_channel(chat_member):
    """Проверяет подписку пользователя на канал."""

    if chat_member.status != 'left':
        return True
    return False


def generate_order_excel(order_items: list, overall_total: float) -> InputFile:
    """Генерирует Excel‑файл с данными заказа и возвращает InputFile для отправки."""

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Заказ"

    ws.append(["Название товара", "Количество", "Общая цена"])

    for item in order_items:
        ws.append([
            item['title'],
            item['quantity'],
            item['total_price']
        ])

    ws.append([])
    ws.append(["Общая сумма", overall_total])

    bio = BytesIO()
    wb.save(bio)
    bio.seek(0)
    return BufferedInputFile(bio.getvalue(), filename="order.xlsx")
