import logging
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .models import Product

logger = logging.getLogger(__name__)


def product_list(request: HttpRequest) -> HttpResponse:
    """
    Отображает каталог всех доступных товаров.

    :param request: HTTP-запрос
    :return: HttpResponse с отрендеренным шаблоном product_list.html
    """
    logger.info("Запрос списка товаров")
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/product_list.html', context)


def product_detail(request: HttpRequest, product_id: int) -> HttpResponse:
    """
    Отображает детальную страницу конкретного товара.
    Обрабатывает случай отсутствия товара мягко (передает None в шаблон).

    :param request: HTTP-запрос
    :param product_id: Уникальный идентификатор товара
    :return: HttpResponse с отрендеренным шаблоном product_detail.html
    """
    logger.info(f"Запрос детали товара: product_id={product_id}")
    try:
        product = Product.objects.get(id=product_id)
        logger.debug(f"Товар найден: {product.name}")
    except Product.DoesNotExist:
        logger.warning(f"Product.DoesNotExist перехвачен. product_id={product_id} не существует.")
        product = None  # Мягкая обработка (Soft Fail)

    context = {'product': product}
    return render(request, 'store/product_detail.html', context)