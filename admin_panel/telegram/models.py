from django.core.validators import (MinValueValidator, MaxValueValidator,
                                    FileExtensionValidator)
from django.db import models


PRICE_MAX_DIGITS: int = 10
PRICE_DECIMAL_PLACES: int = 2
MIN_UNIT_AMOUNT: int = 1
MAX_UNIT_AMOUNT: int = 32000
IMAGE_EXTENSIONS = ('jpg', 'jpeg', 'png', 'gif')


class AbstractModel(models.Model):
    """Абстрактная модель.
    Добавляет наименование и описание."""

    title = models.CharField(
        verbose_name='Наименование',
        unique=True,
        max_length=50
    )
    description = models.TextField(
        verbose_name='Описание',
        max_length=200,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class TgUser(models.Model):
    """Модель пользователя."""

    id = models.BigIntegerField(
        verbose_name='ID пользователя в Telegram',
        primary_key=True,
    )
    username = models.CharField(
        verbose_name='Никнейм',
        max_length=32,
        null=True,
        blank=True,
        default=None,
    )
    bot_unblocked = models.BooleanField(
        verbose_name='Бот разблокирован пользователем',
        default=True
    )
    is_unblocked = models.BooleanField(
        verbose_name='Пользователь разблокирован',
        default=True
    )
    is_subscribed = models.BooleanField(
        verbose_name='Пользователь подписан на канал/группу',
        default=False
    )

    class Meta:
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return f'#{self.id} {self.username}'


class Category(AbstractModel):
    """Модель категории."""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Subcategory(AbstractModel):
    """Модель подкатегории."""

    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        related_name='subcategories',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class Product(AbstractModel):
    """Модель товара."""

    subcategory = models.ForeignKey(
        'Subcategory',
        verbose_name='Подкатегория ',
        related_name='products',
        on_delete=models.CASCADE
    )
    price = models.DecimalField(
        verbose_name='Цена',
        max_digits=PRICE_MAX_DIGITS,
        decimal_places=PRICE_DECIMAL_PLACES,
        validators=[MinValueValidator(0)],
    )
    image = models.ImageField(
        upload_to='product_images',
        verbose_name='Изображение',
        default='',
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=IMAGE_EXTENSIONS
            )
        ],
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f'{self.title} - {self.price} р.'


class ShoppingCart(models.Model):
    """Модель корзины."""

    user = models.ForeignKey(
        TgUser,
        verbose_name='Пользователь корзины',
        on_delete=models.CASCADE,
        related_name='users'
    )
    products = models.ManyToManyField(
        Product,
        through='ShoppingCartProducts',
        verbose_name='Список товаров',
    )

    class Meta:
        verbose_name = 'Корзина покупок'
        verbose_name_plural = 'Корзины покупок'


class ShoppingCartProducts(models.Model):
    """Промежуточная таблица для модели корзины.
    Устанавливает связь M:M с таблицей ShoppingCart."""

    shopping_cart = models.ForeignKey(
        ShoppingCart,
        verbose_name='Корзина покупок',
        on_delete=models.CASCADE,
        related_name='cart_products'
    )
    product = models.ForeignKey(
        Product,
        verbose_name='Продукты',
        on_delete=models.CASCADE,
        related_name='products'
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Количество',
        default=1,
        validators=[
            MinValueValidator(
                MIN_UNIT_AMOUNT,
                message='Количество не может быть меньше 1 единицы!'),
            MaxValueValidator(
                MAX_UNIT_AMOUNT,
                message='Количество не может быть больше 32000 единиц!'
            )
        ]
    )

    class Meta:
        verbose_name_plural = 'Количество товаров'
        constraints = [
            models.UniqueConstraint(
                fields=['shopping_cart', 'product'],
                name='unique_shopping_cart_product',
                violation_error_message='Товар уже есть в корзине!'
            )
        ]

    def __str__(self):
        return f'{self.product.title}: {self.quantity} шт.'

    @property
    def total_price(self):
        return self.product.price * self.quantity
