from datetime import datetime, timedelta
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.http import HttpRequest
from django.shortcuts import redirect

from product.models import Product, Handle, Category, Message
from payment.models import DiscountCode
from user.models import MyUser


class FirstTimeVisitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'role' in request.session.keys():
            request.session['visited_before'] = True
            if 'expire_at' not in request.session.keys():
                request.session['expire_at'] = (
                    timezone.localtime(timezone.now()) + timedelta(seconds=3600)).isoformat()

        else:
            request.session['visited_before'] = False
        response = self.get_response(request)

        return response


class SessionExpirationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):

        if 'expire_at' in request.session.keys() and parse_datetime(request.session['expire_at']) < timezone.localtime(timezone.now()):
            if request.user.is_superuser:
                request.session.clear()
                return redirect('home')
            elif request.session['role'] == 'staff' and request.user.is_authenticated:
                user = MyUser.objects.get(id=request.user.id)
                prod = Product.objects.filter(add_by=user)
                handle = Handle.objects.filter(add_by=user)
                category = Category.objects.filter(
                    add_by=user)
                # message =
                prod.delete()
                handle.delete()
                category.delete()

                user.is_active = False
                user.save()

            request.session.clear()
            return redirect('home')
        response = self.get_response(request)
        return response
