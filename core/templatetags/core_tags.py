from django import template

register = template.Library()


@register.filter
def dict_key_with_var(dict: dict, var: str):

    return dict[var]


@register.filter
def even_n(it):
    return True if it % 2 == 0 else False
