from django import template

register = template.Library()


@register.filter
def currency(value):
    """
    Форматирует число в красивую валютную строку с пробелами и знаком ₽.
    Пример: 12345.67 -> '12 345,67 ₽'
    """
    if value is None:
        return "0,00 ₽"
    return f"{value:,.2f}".replace(",", " ").replace(".", ",") + " ₽"