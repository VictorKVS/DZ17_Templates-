import logging
from django.db import models

logger = logging.getLogger(__name__)


class Product(models.Model):
    """
    Модель товара интернет-магазина.
    Инвариант: цена всегда имеет 2 знака после запятой, дата создается автоматически.
    """
    name = models.CharField(
        max_length=200,
        verbose_name="Название товара",
        help_text="Краткое и понятное название продукта"
    )
    description = models.TextField(
        verbose_name="Описание товара",
        help_text="Подробное описание характеристик и преимуществ"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена (₽)",
        help_text="Стоимость товара с точностью до копеек"
    )
    image = models.ImageField(
        upload_to='products/%Y/%m/',
        verbose_name="Изображение",
        help_text="Фотография товара (рекомендуется 1:1 или 4:3)",
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
        help_text="Автоматически заполняется при создании"
    )

    class Meta:
        ordering = ['-created_at']  # Новые товары сверху
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self) -> str:
        return f"{self.name} ({self.price} ₽)"