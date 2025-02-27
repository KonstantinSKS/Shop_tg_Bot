from aiogram.types.user import User
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User as Model_User

from admin_panel.telegram.models import TgUser, Product, Category, Subcategory


@sync_to_async()
def create_super_user(username, password):  # НАДО
    """Автоматическое создание логина и пароля для суперпользователя."""

    if not Model_User.objects.filter(username=username).exists():
        Model_User.objects.create_superuser(username, password=password)


@sync_to_async
def get_tg_user(user_id):  # НАДО
    """Возвращает экземпляр требуемого пользователя по id."""

    return TgUser.objects.filter(id=user_id, is_subscribed=True).first()


@sync_to_async()  # НАДО
def tg_user_exists(tg_user_id: int) -> bool:
    """Проверка наличия пользователя в БД по tg_id и проверка его подписки."""

    return TgUser.objects.filter(id=tg_user_id).exists()


# @sync_to_async()
# def update_user_token(tg_user_id: int, token: str):
#     """Обновляет токен пользователя в БД."""

#     return TgUser.objects.filter(id=tg_user_id).aupdate(token=token)


@sync_to_async
def create_tg_user(user: User, is_subscribed: bool):  # НАДО
    """Создаёт и возвращает экземпляр пользователя TgUser."""

    tg_user = TgUser.objects.create(
        id=user.id,
        username=user.username,
        is_subscribed=is_subscribed
    )
    return tg_user


@sync_to_async
def get_all_categories():  # НАДО
    """Возвращает все категории товаров."""

    return Category.objects.all()
