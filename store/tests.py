from django.test import TestCase
from django.urls import reverse
from .models import Product
from decimal import Decimal


class StoreContractTestCase(TestCase):
    """
    Набор тестов, проверяющих соответствие системы строгому контракту.
    Каждый тест проверяет один инвариант из спецификации.
    """

    def setUp(self):
        """Инвариант: Перед каждым тестом создаем эталонный товар."""
        self.product = Product.objects.create(
            name="Эталонный Ноутбук",
            description="Мощный и легкий, идеален для работы.",
            price=Decimal('150000.50'),
        )

    def test_01_model_creation_and_str(self):
        """Гарантия: Модель создается и корректно преобразуется в строку."""
        self.assertEqual(str(self.product), "Эталонный Ноутбук (150000.50 ₽)")
        self.assertEqual(self.product.price, Decimal('150000.50'))

    def test_02_product_list_view_status_and_context(self):
        """Гарантия: Список возвращает 200 OK и содержит товары в контексте."""
        url = reverse('store:product_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Эталонный Ноутбук")
        self.assertIn('products', response.context)

    def test_03_product_detail_view_found(self):
        """Гарантия: Детальная страница существующего товара возвращает 200 OK."""
        url = reverse('store:product_detail', kwargs={'product_id': self.product.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Мощный и легкий")

    def test_04_product_detail_view_not_found_soft_fail(self):
        """
        КРИТИЧНО: Запрос несуществующего товара НЕ вызывает 500/404,
        а рендерит шаблон с сообщением "Товар не найден".
        Это требование ТЗ "Обработка ошибок".
        """
        url = reverse('store:product_detail', kwargs={'product_id': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # Мягкая обработка!
        self.assertContains(response, "Товар не найден")
        self.assertIsNone(response.context['product'])