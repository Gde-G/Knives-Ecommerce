from django import template

register = template.Library()


@register.filter
def float_num_digit(num):
    return str(round(num, 2))
