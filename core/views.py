from django.shortcuts import render
from django.http import HttpRequest


def index(request: HttpRequest):
    return render(request, 'core/index.html')


def private_policy(request: HttpRequest):
    return render(request, 'core/privacy_policy.html')


def term_use(request: HttpRequest):
    return render(request, 'core/terms_conditions.html')


def error_403(request: HttpRequest, exception):
    return render(request, 'core/error-403.html')


def error_404(request: HttpRequest, exception):
    return render(request, 'core/error-404.html')


def error_500(request: HttpRequest):
    return render(request, 'core/error-500.html')
