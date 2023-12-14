from django.http import HttpRequest

from .utils import path_as_list


def breadcrumb_path(request: HttpRequest):
    return {'breadcrumb': path_as_list(request)}
