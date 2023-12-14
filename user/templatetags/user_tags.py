from django import template
from django.utils import timezone
from django.template.defaultfilters import stringfilter
from user.models import MyUser
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def search_term(content, term):

    return not (term in content)
