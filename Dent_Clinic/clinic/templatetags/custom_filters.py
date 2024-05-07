from django import template

register = template.Library()


@register.filter
def multiply_string(value, times):
    return value * times
