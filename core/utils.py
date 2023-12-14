from django.http import HttpRequest
from django.apps import apps


def path_as_list(request: HttpRequest):
    name_path = {}
    arr = request.path_info[1:-1].split('/')
    for x in range(len(arr)):
        if x == 0:
            name_path[arr[x]] = '/' + arr[x] + '/'
        else:
            name_path[arr[x]] = arr[x-1] + '/' + arr[x] + '/'

    return name_path


def get_models_in_app(app_label):
    try:
        app_config = apps.get_app_config(app_label)
        models_in_app = app_config.get_models()
        return models_in_app
    except LookupError:
        return None
