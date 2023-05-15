from django import template

register = template.Library()


@register.filter
def star_range(value, max_value=None):
    if max_value is None:
        max_value = value
        value = 0
    return list(range(int(value), int(max_value)))


@register.filter
def subtract(value, arg):
    return value - arg


@register.filter
def int_filter(value):
    return int(value)