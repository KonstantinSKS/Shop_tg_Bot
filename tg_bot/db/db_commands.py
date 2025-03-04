from django.utils import timezone

from aiogram.types.user import User
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User as Model_User

from admin_panel.telegram.models import (
    Mailing, TgUser, Product, Category, Subcategory,
    ShoppingCart, ShoppingCartProducts, DeliveryAddress)


@sync_to_async()
def create_super_user(username, password):
    """Автоматическое создание логина и пароля для суперпользователя."""

    if not Model_User.objects.filter(username=username).exists():
        Model_User.objects.create_superuser(username, password=password)


@sync_to_async
def get_tg_user(user_id):
    """Возвращает экземпляр требуемого пользователя по id."""

    return TgUser.objects.filter(id=user_id, is_subscribed=True).first()


@sync_to_async()
def tg_user_exists(tg_user_id: int) -> bool:
    """Проверка наличия пользователя в БД по tg_id и проверка его подписки."""

    return TgUser.objects.filter(id=tg_user_id).exists()


@sync_to_async
def create_tg_user(user: User, is_subscribed: bool):
    """Создаёт и возвращает экземпляр пользователя TgUser."""

    tg_user = TgUser.objects.create(
        id=user.id,
        username=user.username,
        is_subscribed=is_subscribed
    )
    return tg_user


@sync_to_async
def get_all_categories():
    """Возвращает все категории товаров."""

    return Category.objects.all()


@sync_to_async
def get_category(category_id):
    """Возвращает экземпляр требуемой категории по id."""

    return Category.objects.filter(id=category_id).first()


@sync_to_async
def get_all_subcategories(category_id):
    """Возвращает все связанные подкатегории товаров."""

    return Subcategory.objects.filter(category_id=category_id)


@sync_to_async
def get_subcategory(subcategory_id):
    """Возвращает экземпляр требуемой подкатегории по id."""

    return Subcategory.objects.filter(id=subcategory_id).first()


@sync_to_async
def get_all_products(subcategory_id):
    """Возвращает все связанные товары."""

    return Product.objects.filter(subcategory_id=subcategory_id)


@sync_to_async
def get_related_product(subcategory_id):
    """Возвращает экземпляр товара связанного с подкатегорией по id."""

    return Product.objects.filter(subcategory__id=subcategory_id).first()


@sync_to_async
def get_product(product_id):
    """Возвращает экземпляр требуемого товара по id."""

    return Product.objects.filter(id=product_id).first()


@sync_to_async
def create_or_add_to_cart(user: TgUser, product_data: list):
    """Создает корзину (если не создана) для пользователя.
    Добавляет продукты."""

    cart, created = ShoppingCart.objects.get_or_create(user=user)
    for product_data in product_data:
        product_id = product_data.get('id')
        quantity = product_data.get('quantity', 1)
        cart_product, cp_created = ShoppingCartProducts.objects.get_or_create(
            shopping_cart=cart,
            product_id=product_id,
            defaults={'quantity': quantity}
        )
        if not cp_created:
            cart_product.quantity += quantity
            cart_product.save()
    return cart


@sync_to_async
def get_cart(tg_user):
    """Возвращает экземпляр корзины связанной с пользователем по id."""

    return ShoppingCart.objects.filter(user=tg_user).first()


@sync_to_async
def create_delivery_address(user: TgUser, address: str):
    """Создает или обновляет адрес доставки для пользователя."""
    delivery_addr, created = DeliveryAddress.objects.update_or_create(
        user=user,
        defaults={'address': address}
    )
    return delivery_addr


@sync_to_async
def get_unblocked_users():
    """Возвращает всех незаблокированных пользователей"""
    return TgUser.objects.filter(
        bot_unblocked=True,
        is_unblocked=True,
    )


@sync_to_async
def get_unsent_mailings():
    """Возвращает все неразосланные рассылки, чье время отправки наступило"""
    return Mailing.objects.filter(
        date_mailling__lte=timezone.now(),
        is_sent=False,
    )


@sync_to_async
def save_model(model):
    """Сохранение изменений в модели"""
    model.save()
